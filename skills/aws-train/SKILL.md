---
name: aws-train
description: "Train models on SageMaker with built-in algorithms, custom containers, spot instances, and hyperparameter tuning."
aliases: [sagemaker train, aws training, sagemaker tuning, aws model training]
extends: ml-automation
user_invocable: true
---

# AWS Train

Train a model on SageMaker using built-in algorithms (XGBoost, Linear Learner, Image Classification) or custom ECR containers. Supports managed spot training for cost savings, distributed multi-instance training, and Bayesian hyperparameter tuning with configurable search spaces.

## Full Specification

See `commands/aws-train.md` for the complete workflow.
