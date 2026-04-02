---
name: aws-deploy
description: "Deploy ML models to SageMaker endpoints, Lambda functions, or ECS containers with autoscaling and monitoring."
aliases: [sagemaker deploy, aws endpoint, lambda deploy, aws inference, serverless deploy]
extends: spark
user_invocable: true
---

# AWS Deploy

Deploy trained models to AWS infrastructure. Supports SageMaker real-time and serverless endpoints, Lambda functions with API Gateway, and ECS/Fargate containers with load balancing. Configures autoscaling, runs smoke tests, measures latency (p50/p95/p99), and sets up CloudWatch monitoring with alarms.

## When to Use

- You have a trained model artifact in S3 and need to serve it for real-time inference.
- You want to compare deployment targets (SageMaker endpoint vs. Lambda vs. ECS) for cost and latency.
- You need autoscaling configured automatically based on traffic patterns.
- You want a smoke test and latency benchmark before routing production traffic.

## Workflow

1. **Env Check** -- Verify AWS credentials, SageMaker SDK, and permissions for the target service (SageMaker, Lambda, or ECS).
2. **Model Resolution** -- Locate the model artifact at the given S3 URI. If a SageMaker Model Registry ARN is provided, resolve it to the underlying S3 path.
3. **Deployment** -- Deploy to the selected target:
   - `endpoint` -- Create a SageMaker Model, EndpointConfig, and Endpoint (real-time or serverless). Configure autoscaling if `--autoscale` is set.
   - `lambda` -- Package the model into a Lambda deployment package, create the function with an API Gateway trigger.
   - `ecs` -- Build a Fargate task definition with the model container, create an ECS service behind an ALB.
4. **Smoke Test** -- Send sample inference requests, measure p50/p95/p99 latency, and verify response schema correctness.

Agent: `aws-deployer`.

## Report Bus Integration

| Report key          | Key fields                                                             |
|---------------------|------------------------------------------------------------------------|
| `aws_deploy_report` | `endpoint_name`, `target`, `latency_p95`, `autoscale`, `smoke_passed` |

## Full Specification

Usage: `/aws-deploy <model_s3_uri> [--target endpoint|lambda|ecs] [--autoscale]`

See `commands/aws-deploy.md` for the complete workflow.
