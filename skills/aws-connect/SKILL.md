---
name: aws-connect
description: "Configure AWS credentials, profiles, regions, and SSO for ML workflows. Verify connectivity and permissions."
aliases: [aws credentials, aws setup, aws login, aws configure]
extends: ml-automation
user_invocable: true
---

# AWS Connect

Configure AWS credentials and verify connectivity for ML workflows. Supports named profiles, region selection, and SSO authentication. Validates SageMaker, S3, and IAM permissions and creates project-level AWS configuration.

## When to Use

- You are setting up AWS access for the first time in a project.
- You need to switch between AWS profiles or regions.
- You want to authenticate via AWS SSO instead of static credentials.
- You need to verify that your credentials have the required ML permissions (SageMaker, S3, IAM).

## Workflow

1. **Env Check** -- Verify that the AWS CLI and boto3 are installed. Check for existing `~/.aws/credentials` and `~/.aws/config` files.
2. **Credential Discovery** -- Resolve credentials from the specified profile, SSO session, environment variables, or instance metadata (in that priority order). If `--sso` is set, initiate the SSO login flow.
3. **Validation** -- Call `sts:GetCallerIdentity` to confirm authentication, then probe key services (S3 `ListBuckets`, SageMaker `ListEndpoints`, IAM `GetUser`) to verify permissions. Write a project-level `aws_config.json` with the active profile and region.

## Report Bus Integration

| Report key           | Key fields                                              |
|----------------------|---------------------------------------------------------|
| `aws_connect_report` | `account_id`, `profile`, `region`, `permissions`, `sso` |

## Full Specification

Usage: `/aws-connect [--profile <name>] [--region <region>] [--sso]`

See `commands/aws-connect.md` for the complete workflow.
