---
name: aws-data
description: "Manage S3 data: upload, download, catalog with Glue, query with Athena, and profile datasets."
aliases: [s3 upload, s3 download, glue catalog, athena query, aws data management]
extends: ml-automation
user_invocable: true
---

# AWS Data

Manage S3 data for ML workflows. Upload and download with multipart transfers, catalog datasets with Glue crawlers for automatic schema discovery, run Athena SQL queries on cataloged data, list S3 objects, and profile datasets with statistical summaries (types, nulls, distributions).

## When to Use

- You need to upload local data to S3 or download S3 objects to your machine.
- You want to catalog a dataset in AWS Glue for schema discovery and downstream Athena queries.
- You need to run SQL queries against S3 data via Athena without spinning up infrastructure.
- You want a quick statistical profile (types, nulls, distributions) of an S3 dataset.

## Workflow

1. **Env Check** -- Verify AWS credentials and boto3 availability. Confirm S3 and (if needed) Glue/Athena permissions.
2. **Action Execution** -- Run the requested action:
   - `upload` -- Multipart upload of local files or directories to an S3 URI.
   - `download` -- Recursive download from an S3 prefix to a local path.
   - `catalog` -- Create or update a Glue crawler, run it, and return the discovered schema.
   - `query` -- Execute an Athena SQL query against cataloged data and return results.
   - `list` -- List objects under an S3 prefix with size and last-modified metadata.
   - `profile` -- Download a sample, compute column statistics, and return a profiling summary.

Agent: `aws-data-engineer`.

## Report Bus Integration

| Report key        | Key fields                                                   |
|-------------------|--------------------------------------------------------------|
| `aws_data_report` | `action`, `s3_uri`, `file_count`, `total_size`, `duration_s` |

## Full Specification

Usage: `/aws-data <action> [options]`

Actions: `upload`, `download`, `catalog`, `query`, `list`, `profile`.

See `commands/aws-data.md` for the complete workflow.
