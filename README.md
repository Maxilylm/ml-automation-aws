# ml-automation-aws

AWS ML platform extension for [ml-automation](https://github.com/Maxilylm/ml-automation-core).

## Prerequisites

- [ml-automation](https://github.com/Maxilylm/ml-automation-core) core plugin (>= v1.8.0)
- Claude Code CLI
- AWS CLI configured with valid credentials
- AWS SDK: `boto3`, `sagemaker` (installed automatically by commands)

## Installation

```bash
claude plugin add /path/to/ml-automation-aws
```

## What's Included

### Agents

| Agent | Purpose | Hooks Into |
|---|---|---|
| `aws-ml-engineer` | SageMaker training, hyperparameter tuning, model registry | `before-deploy` |
| `aws-data-engineer` | S3 data management, Glue ETL, Athena queries | `after-init` |
| `aws-deployer` | Deploy to SageMaker endpoints, Lambda, ECS/ECR | *(direct invocation)* |
| `aws-reviewer` | AWS cost, security, and best practices review | `after-evaluation` |

### Commands

| Command | Purpose |
|---|---|
| `/aws-connect` | Configure AWS credentials (profiles, regions, SSO) |
| `/aws-coldstart` | Full AWS ML workflow (S3 -> SageMaker -> deploy) |
| `/aws-train` | Train model on SageMaker (built-in algos, custom containers, tuning) |
| `/aws-deploy` | Deploy to SageMaker endpoint, Lambda, or ECS |
| `/aws-pipeline` | Build SageMaker Pipeline (processing -> training -> eval -> deploy) |
| `/aws-data` | Manage S3 data (upload, download, catalog, query) |
| `/aws-status` | Check AWS resources (endpoints, jobs, buckets, costs) |

## Getting Started

```bash
# Configure AWS credentials
/aws-connect --profile my-profile --region us-east-1

# Full workflow: data -> train -> deploy
/aws-coldstart data.csv --algorithm xgboost --target label --deploy endpoint

# Train on SageMaker with spot instances
/aws-train s3://bucket/data/ --algorithm xgboost --spot --tune --max-jobs 20

# Deploy a trained model
/aws-deploy s3://bucket/output/model.tar.gz --target endpoint --autoscale

# Build a SageMaker Pipeline
/aws-pipeline s3://bucket/raw-data/ --algorithm xgboost --deploy --schedule "cron(0 8 * * ? *)"

# Manage S3 data
/aws-data upload ./data/ s3://bucket/ml-data/
/aws-data catalog s3://bucket/ml-data/
/aws-data query "SELECT * FROM ml_db.training_data LIMIT 10"

# Check resource status and costs
/aws-status --resource all --days 30
```

## How It Integrates

When installed alongside the core plugin:

1. **Automatic routing** -- Tasks mentioning SageMaker, S3, Lambda, ECR, or AWS ML are routed to AWS agents
2. **Core workflow hooks** -- When running `/team-coldstart`:
   - `aws-data-engineer` fires at `after-init` to detect and manage S3 data
   - `aws-ml-engineer` fires at `before-deploy` to configure SageMaker training
   - `aws-reviewer` fires at `after-evaluation` to review AWS configurations
3. **Core agent reuse** -- Commands use eda-analyst, developer, ml-theory-advisor from core

## License

MIT
