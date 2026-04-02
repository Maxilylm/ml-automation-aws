"""
AWS utilities for the ml-automation-aws extension plugin.

Requires ml_utils.py from the ml-automation core plugin to be present
in the same directory (copied via Stage 0 of AWS commands).
"""

import json
import time
from pathlib import Path
from typing import Dict, Optional, Any, List


# --- Relevance Detection ---

AWS_INDICATORS = {
    "boto3",
    "sagemaker",
    "awscli",
    "aws-cdk-lib",
    "moto",
    "s3fs",
    "aiobotocore",
    "aws-lambda-powertools",
    "aws-sam-cli",
}

AWS_SERVICE_PATTERNS = [
    r"s3://",
    r"arn:aws:",
    r"sagemaker",
    r"lambda",
    r"ecr\..*\.amazonaws\.com",
    r"AWS_ACCESS_KEY_ID",
    r"AWS_SECRET_ACCESS_KEY",
    r"AWS_PROFILE",
]


def detect_aws_relevance(project_path="."):
    """Check if project has AWS/ML indicators for relevance gating.

    Checks: AWS library imports, S3 URIs, ARN references, AWS config files,
    SageMaker artifacts, CloudFormation/CDK templates.

    Args:
        project_path: root directory of the project

    Returns:
        dict with 'is_aws': bool, 'indicators': list of found indicators
    """
    import re

    indicators = []
    project = Path(project_path)

    # Check for AWS config files
    aws_configs = [
        "aws_config.json",
        "samconfig.toml",
        "template.yaml",
        "template.json",
        "cdk.json",
        "serverless.yml",
    ]
    for config_file in aws_configs:
        if (project / config_file).exists():
            indicators.append(f"AWS config file: {config_file}")

    # Check for ~/.aws/ credentials
    aws_dir = Path.home() / ".aws"
    if (aws_dir / "credentials").exists():
        indicators.append("AWS credentials file found (~/.aws/credentials)")

    # Check requirements for AWS packages
    for req_file in ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]:
        req_path = project / req_file
        if req_path.exists():
            content = req_path.read_text().lower()
            for pkg in AWS_INDICATORS:
                if pkg in content:
                    indicators.append(f"{pkg} in {req_file}")

    # Check Python files for AWS imports and S3 URIs
    py_files = list(project.glob("**/*.py"))[:50]  # limit scan
    for py_file in py_files:
        try:
            content = py_file.read_text()
            for pkg in AWS_INDICATORS:
                if f"import {pkg}" in content or f"from {pkg}" in content:
                    indicators.append(f"{pkg} import in {py_file.name}")
                    break
            for pattern in AWS_SERVICE_PATTERNS:
                if re.search(pattern, content):
                    indicators.append(f"AWS reference in {py_file.name}: {pattern}")
                    break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for CloudFormation / CDK / Terraform AWS templates
    for ext in ["*.yaml", "*.yml", "*.json"]:
        for tpl_file in list(project.glob(ext))[:20]:
            try:
                content = tpl_file.read_text()
                if "AWS::" in content or "aws_" in content:
                    indicators.append(f"AWS template: {tpl_file.name}")
                    break
            except (UnicodeDecodeError, PermissionError):
                continue

    # Check for SageMaker artifacts
    tar_files = list(project.glob("**/model.tar.gz"))
    if tar_files:
        indicators.append(f"{len(tar_files)} model.tar.gz files (SageMaker artifacts)")

    return {
        "is_aws": len(indicators) > 0,
        "indicators": indicators,
    }


# --- AWS Session Management ---

def get_aws_session(profile: Optional[str] = None, region: Optional[str] = None):
    """Create a boto3 session with the specified profile and region.

    Falls back to: aws_config.json -> environment variables -> default profile.

    Args:
        profile: AWS CLI profile name (optional)
        region: AWS region (optional)

    Returns:
        boto3.Session object

    Raises:
        ImportError: if boto3 is not installed
        RuntimeError: if credentials are invalid
    """
    try:
        import boto3
    except ImportError:
        raise ImportError(
            "boto3 required. Install with: pip install boto3"
        )

    # Try loading from project config
    config_path = Path("aws_config.json")
    config = {}
    if config_path.exists():
        config = json.loads(config_path.read_text())

    session_kwargs = {}
    if profile or config.get("profile"):
        session_kwargs["profile_name"] = profile or config["profile"]
    if region or config.get("region"):
        session_kwargs["region_name"] = region or config["region"]

    session = boto3.Session(**session_kwargs)

    # Verify credentials
    sts = session.client("sts")
    try:
        identity = sts.get_caller_identity()
    except Exception as e:
        raise RuntimeError(
            f"AWS credential verification failed: {e}. "
            f"Run /aws-connect to configure credentials."
        )

    return session


# --- S3 Operations ---

def upload_to_s3(local_path: str, s3_uri: str, session=None) -> Dict[str, Any]:
    """Upload a file or directory to S3.

    Handles multipart uploads for large files and recursive directory uploads.

    Args:
        local_path: local file or directory path
        s3_uri: S3 URI (s3://bucket/key)
        session: boto3 session (optional, creates default if None)

    Returns:
        dict with 'uploaded': list of S3 URIs, 'total_size': bytes,
        'file_count': int, 'duration_seconds': float
    """
    if session is None:
        session = get_aws_session()

    s3 = session.client("s3")
    bucket, prefix = _parse_s3_uri(s3_uri)
    local = Path(local_path)
    uploaded = []
    total_size = 0
    start = time.time()

    if local.is_file():
        key = prefix + "/" + local.name if prefix else local.name
        file_size = local.stat().st_size
        s3.upload_file(str(local), bucket, key)
        uploaded.append(f"s3://{bucket}/{key}")
        total_size += file_size
    elif local.is_dir():
        for file_path in local.rglob("*"):
            if file_path.is_file():
                relative = file_path.relative_to(local)
                key = f"{prefix}/{relative}" if prefix else str(relative)
                file_size = file_path.stat().st_size
                s3.upload_file(str(file_path), bucket, key)
                uploaded.append(f"s3://{bucket}/{key}")
                total_size += file_size
    else:
        raise FileNotFoundError(f"Local path not found: {local_path}")

    duration = time.time() - start

    return {
        "uploaded": uploaded,
        "total_size": total_size,
        "file_count": len(uploaded),
        "duration_seconds": round(duration, 2),
    }


def download_from_s3(s3_uri: str, local_path: str, session=None) -> Dict[str, Any]:
    """Download a file or prefix from S3 to local filesystem.

    Args:
        s3_uri: S3 URI (s3://bucket/key or s3://bucket/prefix/)
        local_path: local directory to download into
        session: boto3 session (optional)

    Returns:
        dict with 'downloaded': list of local paths, 'total_size': bytes,
        'file_count': int, 'duration_seconds': float
    """
    if session is None:
        session = get_aws_session()

    s3 = session.client("s3")
    bucket, prefix = _parse_s3_uri(s3_uri)
    local = Path(local_path)
    local.mkdir(parents=True, exist_ok=True)
    downloaded = []
    total_size = 0
    start = time.time()

    # List objects with prefix
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            relative_key = key[len(prefix):].lstrip("/") if prefix else key
            if not relative_key:
                continue
            dest = local / relative_key
            dest.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(bucket, key, str(dest))
            downloaded.append(str(dest))
            total_size += obj["Size"]

    duration = time.time() - start

    return {
        "downloaded": downloaded,
        "total_size": total_size,
        "file_count": len(downloaded),
        "duration_seconds": round(duration, 2),
    }


def _parse_s3_uri(s3_uri: str):
    """Parse s3://bucket/key into (bucket, key)."""
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {s3_uri}. Must start with s3://")
    parts = s3_uri[5:].split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    return bucket, key


# --- SageMaker Operations ---

def create_sagemaker_estimator(
    algorithm: str = "xgboost",
    instance_type: str = "ml.m5.xlarge",
    instance_count: int = 1,
    hyperparameters: Optional[Dict] = None,
    role: Optional[str] = None,
    spot: bool = False,
    session=None,
) -> Any:
    """Create a SageMaker Estimator for training.

    Args:
        algorithm: built-in algorithm name or ECR image URI
        instance_type: training instance type
        instance_count: number of training instances
        hyperparameters: algorithm hyperparameters
        role: SageMaker execution role ARN (auto-detect if None)
        spot: use managed spot training
        session: boto3 session (optional)

    Returns:
        sagemaker.estimator.Estimator object
    """
    try:
        import sagemaker
        from sagemaker import image_uris
    except ImportError:
        raise ImportError(
            "sagemaker SDK required. Install with: pip install sagemaker"
        )

    if session is None:
        session = get_aws_session()

    sagemaker_session = sagemaker.Session(boto_session=session)

    # Resolve role
    if role is None:
        config_path = Path("aws_config.json")
        if config_path.exists():
            config = json.loads(config_path.read_text())
            role = config.get("sagemaker_role")
        if role is None:
            role = sagemaker.get_execution_role()

    # Resolve container image
    region = session.region_name
    builtin_algorithms = {
        "xgboost": "xgboost",
        "linear": "linear-learner",
        "linear-learner": "linear-learner",
        "image-classification": "image-classification",
        "object-detection": "object-detection",
        "knn": "knn",
        "kmeans": "kmeans",
        "pca": "pca",
        "factorization-machines": "factorization-machines",
    }

    if algorithm in builtin_algorithms:
        image_uri = image_uris.retrieve(
            framework=builtin_algorithms[algorithm],
            region=region,
            version="latest",
        )
    else:
        # Assume it is a custom ECR image URI
        image_uri = algorithm

    # Default hyperparameters per algorithm
    default_hps = {
        "xgboost": {
            "max_depth": "6",
            "eta": "0.3",
            "objective": "binary:logistic",
            "num_round": "100",
            "eval_metric": "auc",
        },
        "linear": {
            "predictor_type": "binary_classifier",
            "mini_batch_size": "200",
        },
    }

    hps = default_hps.get(algorithm, {})
    if hyperparameters:
        hps.update(hyperparameters)

    estimator_kwargs = {
        "image_uri": image_uri,
        "role": role,
        "instance_count": instance_count,
        "instance_type": instance_type,
        "sagemaker_session": sagemaker_session,
        "output_path": f"s3://{sagemaker_session.default_bucket()}/output",
    }

    if spot:
        estimator_kwargs["use_spot_instances"] = True
        estimator_kwargs["max_wait"] = 7200  # 2 hours max wait
        estimator_kwargs["max_run"] = 3600   # 1 hour max run

    estimator = sagemaker.estimator.Estimator(**estimator_kwargs)

    if hps:
        estimator.set_hyperparameters(**hps)

    return estimator


def deploy_sagemaker_endpoint(
    model_data: str,
    instance_type: str = "ml.m5.large",
    initial_instance_count: int = 1,
    endpoint_name: Optional[str] = None,
    serverless: bool = False,
    role: Optional[str] = None,
    session=None,
) -> Dict[str, Any]:
    """Deploy a model to a SageMaker endpoint.

    Args:
        model_data: S3 URI to model.tar.gz
        instance_type: inference instance type
        initial_instance_count: number of instances
        endpoint_name: name for the endpoint (auto-generated if None)
        serverless: use serverless inference
        role: SageMaker execution role ARN
        session: boto3 session (optional)

    Returns:
        dict with 'endpoint_name', 'endpoint_arn', 'status', 'url'
    """
    try:
        import sagemaker
        from sagemaker.model import Model
        from sagemaker.serverless import ServerlessInferenceConfig
    except ImportError:
        raise ImportError(
            "sagemaker SDK required. Install with: pip install sagemaker"
        )

    if session is None:
        session = get_aws_session()

    sagemaker_session = sagemaker.Session(boto_session=session)

    # Resolve role
    if role is None:
        config_path = Path("aws_config.json")
        if config_path.exists():
            config = json.loads(config_path.read_text())
            role = config.get("sagemaker_role")
        if role is None:
            role = sagemaker.get_execution_role()

    # Create model
    model = Model(
        model_data=model_data,
        role=role,
        sagemaker_session=sagemaker_session,
    )

    # Deploy
    deploy_kwargs = {}
    if endpoint_name:
        deploy_kwargs["endpoint_name"] = endpoint_name

    if serverless:
        serverless_config = ServerlessInferenceConfig(
            memory_size_in_mb=2048,
            max_concurrency=10,
        )
        predictor = model.deploy(
            serverless_inference_config=serverless_config,
            **deploy_kwargs,
        )
    else:
        predictor = model.deploy(
            initial_instance_count=initial_instance_count,
            instance_type=instance_type,
            **deploy_kwargs,
        )

    endpoint_name = predictor.endpoint_name
    region = session.region_name
    account = session.client("sts").get_caller_identity()["Account"]

    return {
        "endpoint_name": endpoint_name,
        "endpoint_arn": f"arn:aws:sagemaker:{region}:{account}:endpoint/{endpoint_name}",
        "status": "InService",
        "url": f"https://runtime.sagemaker.{region}.amazonaws.com/endpoints/{endpoint_name}/invocations",
    }


# --- Cost Estimation ---

def get_aws_costs(
    days: int = 7,
    services: Optional[List[str]] = None,
    session=None,
) -> Dict[str, Any]:
    """Get AWS cost breakdown for ML-related services.

    Args:
        days: lookback period in days
        services: list of service names to filter (default: ML services)
        session: boto3 session (optional)

    Returns:
        dict with 'total': float, 'by_service': dict, 'period': dict,
        'currency': str
    """
    if session is None:
        session = get_aws_session()

    ce = session.client("ce")

    from datetime import datetime, timedelta
    end_date = datetime.utcnow().strftime("%Y-%m-%d")
    start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Default ML-related services
    if services is None:
        services = [
            "Amazon SageMaker",
            "Amazon Simple Storage Service",
            "AWS Lambda",
            "AWS Glue",
            "Amazon Elastic Container Service",
            "Amazon Elastic Container Registry Public",
            "Amazon Athena",
        ]

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": services,
                }
            },
        )
    except Exception as e:
        return {
            "error": str(e),
            "total": 0.0,
            "by_service": {},
            "period": {"start": start_date, "end": end_date},
            "currency": "USD",
        }

    # Aggregate costs by service
    by_service = {}
    total = 0.0

    for result in response.get("ResultsByTime", []):
        for group in result.get("Groups", []):
            service_name = group["Keys"][0]
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
            by_service[service_name] = by_service.get(service_name, 0.0) + amount
            total += amount

    # Round values
    by_service = {k: round(v, 2) for k, v in by_service.items()}
    total = round(total, 2)

    return {
        "total": total,
        "by_service": by_service,
        "period": {"start": start_date, "end": end_date},
        "currency": "USD",
    }
