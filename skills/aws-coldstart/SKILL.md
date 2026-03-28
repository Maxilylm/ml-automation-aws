---
name: aws-coldstart
description: "Full AWS ML workflow: S3 data upload, SageMaker training, model evaluation, registry, and deployment in one command."
aliases: [aws ml workflow, aws end to end, sagemaker workflow, aws full pipeline]
extends: ml-automation
user_invocable: true
---

# AWS Coldstart

End-to-end AWS ML workflow that uploads data to S3, trains a model on SageMaker (built-in algorithms or custom containers), evaluates on a held-out test set, registers in SageMaker Model Registry, deploys to an endpoint (SageMaker, Lambda, or ECS), and provides a cost summary.

## Full Specification

See `commands/aws-coldstart.md` for the complete workflow.
