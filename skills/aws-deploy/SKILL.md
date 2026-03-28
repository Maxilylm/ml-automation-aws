---
name: aws-deploy
description: "Deploy ML models to SageMaker endpoints, Lambda functions, or ECS containers with autoscaling and monitoring."
aliases: [sagemaker deploy, aws endpoint, lambda deploy, aws inference, serverless deploy]
extends: ml-automation
user_invocable: true
---

# AWS Deploy

Deploy trained models to AWS infrastructure. Supports SageMaker real-time and serverless endpoints, Lambda functions with API Gateway, and ECS/Fargate containers with load balancing. Configures autoscaling, runs smoke tests, measures latency (p50/p95/p99), and sets up CloudWatch monitoring with alarms.

## Full Specification

See `commands/aws-deploy.md` for the complete workflow.
