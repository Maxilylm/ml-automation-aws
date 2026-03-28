# /aws-deploy

Deploy a trained model to SageMaker endpoint, Lambda function, or ECS container.

## Usage

```
/aws-deploy <model_s3_uri> [--target endpoint|lambda|ecs] [--instance ml.m5.large] [--serverless] [--autoscale] [--min 1] [--max 4]
```

- `model_s3_uri`: S3 URI to model artifact (`model.tar.gz`) or SageMaker Model Registry ARN
- `--target`: deployment target (default: `endpoint`)
- `--instance`: inference instance type (default: `ml.m5.large`)
- `--serverless`: use SageMaker Serverless Inference (overrides `--instance`)
- `--autoscale`: enable autoscaling
- `--min`: minimum instance count (default: 1)
- `--max`: maximum instance count (default: 4)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Verify AWS credentials and deployment permissions
4. Verify required packages: `boto3`, `sagemaker`

### Stage 1: Model Resolution

1. If S3 URI: verify `model.tar.gz` exists and is accessible
2. If Model Registry ARN: fetch approved model package details
3. Determine inference image:
   - Built-in algorithm: resolve framework container for region
   - Custom: extract ECR URI from model metadata
4. Report: model source, framework, image URI

### Stage 2: Deployment

Based on `--target`:

#### SageMaker Endpoint
1. Create SageMaker Model resource
2. Create endpoint configuration:
   - Instance type and initial instance count
   - If `--serverless`: set memory size and max concurrency
   - Data capture configuration (optional, for monitoring)
3. Create endpoint (or update existing)
4. Wait for endpoint to be `InService`
5. If `--autoscale`: configure target tracking scaling policy

#### Lambda Function
1. Build inference package:
   - Create `lambda_handler.py` with model loading and prediction logic
   - Package model artifact (must be < 250 MB unzipped, or use container)
   - If model > 250 MB: build Docker image and push to ECR
2. Create/update Lambda function
3. Create API Gateway HTTP API with Lambda integration
4. Report: API endpoint URL, function ARN

#### ECS/ECR Container
1. Generate `Dockerfile` with inference server (Flask/FastAPI)
2. Build Docker image and push to ECR
3. Create ECS task definition (Fargate)
4. Create ECS service with Application Load Balancer
5. Configure autoscaling if requested
6. Report: ALB URL, task definition ARN

### Stage 3: Validation

1. Send test inference request to deployed endpoint
2. Verify response format and latency
3. Run 10 warmup requests and measure:
   - p50, p95, p99 latency
   - Throughput (requests/second)
4. Report: validation results, latency profile

### Stage 4: Monitoring Setup

1. Create CloudWatch dashboard with:
   - Invocation count, latency, error rate
   - Instance CPU/memory utilization (for endpoint/ECS)
   - Lambda duration and throttles (for Lambda)
2. Create alarms:
   - Error rate > 1%
   - p99 latency > threshold
   - 5xx error count > 0

### Stage 5: Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-deployer", {
    "status": "completed",
    "target": deploy_target,
    "endpoint_url": endpoint_url,
    "endpoint_arn": endpoint_arn,
    "instance_type": instance_type,
    "autoscaling": autoscale_config,
    "latency": {"p50": p50, "p95": p95, "p99": p99},
    "monthly_cost_estimate": monthly_cost,
    "monitoring": {"dashboard": dashboard_name, "alarms": alarm_names},
    "rollback_config": rollback_info
})
```

Print deployment summary: target, URL, latency, cost estimate, monitoring.
