---
name: aws-status
description: "Check AWS ML resource status: SageMaker endpoints, training jobs, S3 buckets, and cost breakdown."
aliases: [aws resources, aws check, sagemaker status, aws costs, aws dashboard]
extends: ml-automation
user_invocable: true
---

# AWS Status

Check the status of all AWS ML resources. Lists SageMaker endpoints (with idle detection), recent training jobs, S3 bucket summaries, and a cost breakdown by service (SageMaker, S3, Lambda, Glue) with trend comparison against the previous period. Flags alerts for idle resources and cost spikes.

## Full Specification

See `commands/aws-status.md` for the complete workflow.
