---
name: aws-train
description: "Train models on SageMaker with built-in algorithms, custom containers, spot instances, and hyperparameter tuning."
aliases: [sagemaker train, aws training, sagemaker tuning, aws model training]
extends: spark
user_invocable: true
---

# AWS Train

Train a model on SageMaker using built-in algorithms (XGBoost, Linear Learner, Image Classification) or custom ECR containers. Supports managed spot training for cost savings, distributed multi-instance training, and Bayesian hyperparameter tuning with configurable search spaces.

## When to Use

- You have data already in S3 and want to launch a SageMaker training job.
- You want to use spot instances to reduce training costs by up to 90%.
- You need automatic hyperparameter tuning to find the best model configuration.
- You are training with a custom Docker container pushed to ECR.

## Workflow

1. **Env Check** -- Verify AWS credentials, SageMaker SDK, and the SageMaker execution role ARN.
2. **Data Prep** -- Validate the S3 URI, check data format compatibility with the chosen algorithm, and configure train/validation channels.
3. **Training Job** -- Create a SageMaker Estimator with the selected algorithm (or custom image URI), set hyperparameters, configure instance type and count, and launch the training job. If `--spot` is set, enable managed spot training.
4. **Hyperparameter Tuning** -- If `--tune` is set, wrap the estimator in a `HyperparameterTuner` with Bayesian search over the algorithm's default search space, launch the tuning job, and select the best trial.

Agent: `aws-ml-engineer`.

## Report Bus Integration

| Report key            | Key fields                                                       |
|-----------------------|------------------------------------------------------------------|
| `aws_training_report` | `job_name`, `algorithm`, `metrics`, `duration_s`, `cost`, `spot` |

## Full Specification

Usage: `/aws-train <data_s3_uri> [--algorithm xgboost|linear|custom] [--spot] [--tune]`

See `commands/aws-train.md` for the complete workflow.
