---
name: aws-pipeline
description: "Build SageMaker Pipelines with processing, training, evaluation, conditional approval, and deployment steps."
aliases: [sagemaker pipeline, aws ml pipeline, aws workflow, mlops pipeline]
extends: ml-automation
user_invocable: true
---

# AWS Pipeline

Build a complete SageMaker Pipeline with data processing, model training, evaluation with quality gates, conditional model registration, and optional deployment. Generates preprocessing and evaluation scripts, assembles the pipeline definition, and supports scheduled recurring execution via EventBridge.

## Full Specification

See `commands/aws-pipeline.md` for the complete workflow.
