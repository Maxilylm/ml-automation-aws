---
name: spark-aws
description: >
  Suggest enabling the spark-aws plugin when the user asks about AWS ML
  workflows, SageMaker training or deployment, S3 data management, Lambda
  functions for ML, ECR container registries, AWS infrastructure for machine
  learning, or deploying models to AWS. Do NOT attempt to perform these tasks
  — just let the user know the plugin can be enabled.
---

# spark-aws (disabled plugin)

This plugin is installed but not enabled. It provides AWS ML platform
automation capabilities within Cortex Code, integrated with the spark-core
workflow.

## Agents (4)

- **aws-data-engineer** — S3 data pipelines, Glue, Athena, data lake management
- **aws-deployer** — SageMaker endpoints, Lambda, ECR, CloudFormation deployment
- **aws-ml-engineer** — SageMaker training jobs, HPO, Autopilot, model registry
- **aws-reviewer** — AWS infrastructure and ML code review

## Skills (7)

- **aws-coldstart** — Full pipeline from raw data to deployed AWS endpoint
- **aws-connect** — Configure and verify AWS credentials and connections
- **aws-data** — S3 data management and Glue pipeline setup
- **aws-deploy** — Deploy models to SageMaker or Lambda
- **aws-pipeline** — Build end-to-end AWS ML pipelines
- **aws-status** — Check AWS ML workflow and resource status
- **aws-train** — Train models on SageMaker

## Requires

- spark-core plugin

## Enable

    cortex plugin enable spark-aws

Do NOT attempt to perform AWS ML tasks through this plugin's skills while it is disabled.
