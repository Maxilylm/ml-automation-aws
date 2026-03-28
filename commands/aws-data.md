# /aws-data

Manage S3 data: upload, download, catalog with Glue, and query with Athena.

## Usage

```
/aws-data <action> [options]
```

Actions:
- `upload <local_path> <s3_uri>` -- upload files/directory to S3
- `download <s3_uri> <local_path>` -- download from S3 to local
- `catalog <s3_uri>` -- create Glue Data Catalog entry
- `query <sql>` -- run Athena query on cataloged data
- `list [s3_uri]` -- list S3 objects (default: project bucket)
- `profile <s3_uri>` -- data profiling summary of S3 dataset

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Verify AWS credentials
4. Verify required packages: `boto3`, `pandas`, `pyarrow` (for Parquet)

### Action: upload

1. Validate local path exists
2. Determine upload strategy:
   - Single file < 100 MB: simple PUT
   - Single file >= 100 MB: multipart upload with progress
   - Directory: recursive upload with parallel transfers
3. Set content type and metadata
4. Report: uploaded objects, total size, transfer time

### Action: download

1. Validate S3 URI exists
2. Determine download strategy:
   - Single object: simple GET
   - Prefix (directory): recursive download with parallel transfers
3. Create local directory structure
4. Report: downloaded objects, total size, transfer time

### Action: catalog

1. Check if Glue database exists -- create if needed
2. Run or create Glue Crawler:
   - Point to S3 URI
   - Configure classifiers (CSV, Parquet, JSON, ORC)
   - Run crawler and wait for completion
3. Report: database, table name, columns, partitions, row count estimate

### Action: query

1. Verify Athena workgroup and result bucket exist
2. Execute query:
   - Set result output location
   - Submit query execution
   - Poll for completion
   - Fetch results
3. Display results as formatted table (first 50 rows)
4. Report: query execution time, data scanned, cost estimate

### Action: list

1. List S3 objects with prefix
2. Display: key, size, last modified, storage class
3. Summary: total objects, total size, storage class breakdown

### Action: profile

1. Download sample (first 10,000 rows) from S3
2. Compute profiling stats:
   - Column types, null counts, unique values
   - Numeric: min, max, mean, std, percentiles
   - Categorical: top values, cardinality
   - Date: range, gaps
3. Report: profiling summary table

### Final Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-data-engineer", {
    "status": "completed",
    "action": action,
    "s3_uri": s3_uri,
    "details": action_details,
    "cost_estimate": cost
})
```

Print action summary with relevant details.
