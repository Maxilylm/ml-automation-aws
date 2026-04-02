---
name: aws-coldstart
description: "Full AWS ML workflow: S3 data upload, SageMaker training, model evaluation, registry, and deployment in one command."
aliases: [aws ml workflow, aws end to end, sagemaker workflow, aws full pipeline]
extends: spark
user_invocable: true
---

# AWS Coldstart

End-to-end AWS ML workflow that uploads data to S3, trains a model on SageMaker (built-in algorithms or custom containers), evaluates on a held-out test set, registers in SageMaker Model Registry, deploys to an endpoint (SageMaker, Lambda, or ECS), and provides a cost summary.

## When to Use

- You have a local dataset and want a production ML model running on AWS in a single command.
- You need an end-to-end pipeline covering data upload, training, evaluation, registry, and deployment.
- You want to compare built-in SageMaker algorithms (XGBoost, Linear Learner) or bring a custom container.
- You are starting a new AWS ML project and need infrastructure bootstrapped from scratch.

## Workflow

1. **Env Check** -- Verify AWS credentials, boto3/sagemaker SDK, and required IAM permissions (S3, SageMaker, ECR).
2. **S3 Upload** -- Upload the local dataset to S3 with automatic train/test splitting. Agent: `aws-data-engineer`.
3. **SageMaker Training** -- Launch a training job using the selected algorithm, with optional spot instances and hyperparameter defaults. Agent: `aws-ml-engineer`.
4. **Evaluation** -- Run predictions on the held-out test set, compute metrics (AUC, RMSE, accuracy), and apply quality gates.
5. **Registry** -- Register the model artifact in SageMaker Model Registry with metadata, metrics, and lineage tags.
6. **Deploy** -- Deploy to the chosen target (SageMaker endpoint, Lambda, or ECS), run smoke tests, and report latency. Agent: `aws-deployer`.

## Report Bus Integration

Each stage emits a JSON report to the report bus:

| Stage     | Report key              | Key fields                                       |
|-----------|-------------------------|--------------------------------------------------|
| S3 Upload | `aws_data_report`       | `s3_uri`, `file_count`, `total_size`             |
| Training  | `aws_training_report`   | `job_name`, `metrics`, `duration`, `cost`        |
| Evaluate  | `aws_eval_report`       | `test_metrics`, `quality_gate_passed`            |
| Registry  | `aws_registry_report`   | `model_arn`, `model_version`, `tags`             |
| Deploy    | `aws_deploy_report`     | `endpoint_name`, `latency_p95`, `smoke_passed`   |

## Full Specification

Usage: `/aws-coldstart <data_path> [--algorithm xgboost|linear|custom] [--target <col>] [--deploy endpoint|lambda|ecs]`

See `commands/aws-coldstart.md` for the complete workflow.
