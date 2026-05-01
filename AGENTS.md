# spark-aws — Cortex Code Extension

AWS ML platform automation. SageMaker training, S3 data management, Lambda deployment, ECR containers, and AWS ML infrastructure. Requires spark-core installed.

## Available Agents

| Agent | When to use |
|---|---|
| `aws-data-engineer` | User wants to manage S3 data, set up Glue jobs, query with Athena, or build AWS data pipelines |
| `aws-ml-engineer` | User wants to train models on SageMaker, run hyperparameter tuning, or use SageMaker built-in algorithms |
| `aws-deployer` | User wants to deploy to SageMaker endpoints, Lambda, or build ECR containers |
| `aws-reviewer` | User wants cost optimization, security review, or AWS best practices for ML infrastructure |

## Available Skills

| Skill | Trigger |
|---|---|
| `/aws-connect` | "connect to AWS", "configure AWS credentials", "test AWS connection" |
| `/aws-coldstart` | "full AWS ML workflow", "end to end on AWS", "SageMaker coldstart" |
| `/aws-data` | "manage S3 data", "upload to S3", "Glue ETL", "Athena query" |
| `/aws-pipeline` | "AWS data pipeline", "build SageMaker pipeline", "AWS ML workflow" |
| `/aws-train` | "train on SageMaker", "SageMaker training job", "distributed training on AWS" |
| `/aws-deploy` | "deploy to SageMaker", "Lambda deployment", "create ECR container", "AWS endpoint" |
| `/aws-status` | "AWS resource status", "list SageMaker jobs", "check S3 buckets" |

## Routing

- S3, Glue, Athena, data pipelines → `aws-data-engineer`
- SageMaker training, tuning → `aws-ml-engineer`
- Endpoints, Lambda, ECR → `aws-deployer`
- Cost, security, best practices → `aws-reviewer`
- Fallback → spark-core orchestrator
