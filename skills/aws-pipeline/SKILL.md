---
name: aws-pipeline
description: "Build SageMaker Pipelines with processing, training, evaluation, conditional approval, and deployment steps."
aliases: [sagemaker pipeline, aws ml pipeline, aws workflow, mlops pipeline]
extends: ml-automation
user_invocable: true
---

# AWS Pipeline

Build a complete SageMaker Pipeline with data processing, model training, evaluation with quality gates, conditional model registration, and optional deployment. Generates preprocessing and evaluation scripts, assembles the pipeline definition, and supports scheduled recurring execution via EventBridge.

## When to Use

- You need a reproducible, version-controlled ML pipeline on AWS rather than ad-hoc training jobs.
- You want automated quality gates that block deployment when metrics fall below thresholds.
- You need scheduled retraining on a cron cadence (daily, weekly) via EventBridge.
- You are building an MLOps workflow with conditional model registration and approval steps.

## Workflow

1. **Env Check** -- Verify AWS credentials, SageMaker SDK, and the execution role. Confirm S3 access for pipeline artifacts.
2. **Pipeline Design** -- Determine pipeline steps based on arguments: processing, training, evaluation, conditional registration, and optional deployment. Generate preprocessing and evaluation Python scripts.
3. **Steps Configuration** -- Create SageMaker Pipeline step objects:
   - `ProcessingStep` for data preprocessing.
   - `TrainingStep` for model training with the chosen algorithm.
   - `ProcessingStep` (evaluation) for metric computation.
   - `ConditionStep` to gate registration on metric thresholds.
   - `ModelStep` and `EndpointStep` if `--deploy` is set.
4. **Execution** -- Assemble and upsert the pipeline definition, then start execution. If `--schedule` is provided, create an EventBridge rule for recurring runs.

Agent: `aws-ml-engineer`.

## Report Bus Integration

| Report key            | Key fields                                                     |
|-----------------------|----------------------------------------------------------------|
| `aws_pipeline_report` | `pipeline_name`, `pipeline_arn`, `steps`, `schedule`, `status` |

## Full Specification

Usage: `/aws-pipeline <data_s3_uri> [--name <name>] [--deploy] [--schedule <cron>]`

See `commands/aws-pipeline.md` for the complete workflow.
