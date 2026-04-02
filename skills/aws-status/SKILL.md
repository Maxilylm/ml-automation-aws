---
name: aws-status
description: "Check AWS ML resource status: SageMaker endpoints, training jobs, S3 buckets, and cost breakdown."
aliases: [aws resources, aws check, sagemaker status, aws costs, aws dashboard]
extends: ml-automation
user_invocable: true
---

# AWS Status

Check the status of all AWS ML resources. Lists SageMaker endpoints (with idle detection), recent training jobs, S3 bucket summaries, and a cost breakdown by service (SageMaker, S3, Lambda, Glue) with trend comparison against the previous period. Flags alerts for idle resources and cost spikes.

## When to Use

- You want a quick overview of all active SageMaker endpoints and their health.
- You need to check whether recent training jobs succeeded or failed.
- You want a cost breakdown for ML services over the past week with trend analysis.
- You need to identify idle or orphaned resources that are wasting money.

## Workflow

1. **Env Check** -- Verify AWS credentials and permissions for SageMaker, S3, and Cost Explorer APIs.
2. **Resource Queries** -- Query the requested resource types (or all if `--resource all`):
   - `endpoints` -- List SageMaker endpoints with status, instance type, creation time, and idle detection (no invocations in 7 days).
   - `training` -- List recent training jobs with status, duration, billable seconds, and final metrics.
   - `s3` -- List S3 buckets with object count, total size, and storage class breakdown.
3. **Cost Breakdown** -- Query Cost Explorer for the past 7 days, group by service, compute totals, and compare against the previous 7-day period to flag cost spikes (>20% increase).

Agent: `aws-reviewer`.

## Report Bus Integration

| Report key          | Key fields                                                    |
|---------------------|---------------------------------------------------------------|
| `aws_status_report` | `endpoints`, `training_jobs`, `s3_buckets`, `costs`, `alerts` |

## Full Specification

Usage: `/aws-status [--resource endpoints|training|s3|costs|all]`

See `commands/aws-status.md` for the complete workflow.
