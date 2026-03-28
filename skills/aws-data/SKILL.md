---
name: aws-data
description: "Manage S3 data: upload, download, catalog with Glue, query with Athena, and profile datasets."
aliases: [s3 upload, s3 download, glue catalog, athena query, aws data management]
extends: ml-automation
user_invocable: true
---

# AWS Data

Manage S3 data for ML workflows. Upload and download with multipart transfers, catalog datasets with Glue crawlers for automatic schema discovery, run Athena SQL queries on cataloged data, list S3 objects, and profile datasets with statistical summaries (types, nulls, distributions).

## Full Specification

See `commands/aws-data.md` for the complete workflow.
