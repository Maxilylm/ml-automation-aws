# /aws-connect

Configure AWS credentials and verify connectivity for ML workflows.

## Usage

```
/aws-connect [--profile <name>] [--region <region>] [--sso]
```

- `--profile`: AWS CLI profile name (default: `default`)
- `--region`: AWS region (default: `us-east-1`)
- `--sso`: Use AWS SSO for authentication

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Check if AWS CLI is installed (`aws --version`)
4. Check if `boto3` is installed -- if missing, install via `pip install boto3`

### Stage 1: Credential Discovery

1. Check for existing credentials:
   - `~/.aws/credentials` file
   - `~/.aws/config` for named profiles
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
   - EC2 instance metadata (if running on AWS)
   - SSO configuration (`~/.aws/sso/cache/`)
2. If `--sso` flag: run `aws sso login --profile <profile>`
3. Report: credential source, profile name, region

### Stage 2: Connectivity Verification

1. Call `sts:GetCallerIdentity` to verify credentials work
2. Report: account ID, IAM user/role ARN, region
3. Check basic permissions:
   - `s3:ListBuckets` -- can list S3 buckets
   - `sagemaker:ListTrainingJobs` -- can access SageMaker
   - `iam:GetUser` -- can read IAM info
4. Flag missing permissions with suggested IAM policy

### Stage 3: Project Configuration

1. Create or update `aws_config.json` in project root:
   ```json
   {
     "profile": "default",
     "region": "us-east-1",
     "account_id": "123456789012",
     "s3_bucket": "project-name-ml-data",
     "sagemaker_role": "arn:aws:iam::role/SageMakerRole"
   }
   ```
2. Add `aws_config.json` to `.gitignore` if not already present
3. Verify or create default S3 bucket for ML artifacts

### Stage 4: Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-connect", {
    "status": "completed",
    "account_id": account_id,
    "region": region,
    "profile": profile,
    "iam_arn": iam_arn,
    "permissions": {"s3": True, "sagemaker": True, "iam": True},
    "s3_bucket": default_bucket,
    "config_file": "aws_config.json"
})
```

Print connection summary: account, region, permissions, default bucket.
