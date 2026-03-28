# /aws-status

Check AWS ML resource status: SageMaker endpoints, training jobs, S3 buckets, and costs.

## Usage

```
/aws-status [--resource endpoints|training|s3|costs|all] [--days 7]
```

- `--resource`: specific resource type to check (default: `all`)
- `--days`: lookback period for training jobs and costs (default: 7)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Verify AWS credentials
4. Verify `boto3` installed

### Check: SageMaker Endpoints

1. List all SageMaker endpoints in the account/region
2. For each endpoint:
   - Status (InService, Creating, Updating, Failed)
   - Instance type and count
   - Creation date
   - Last invocation time (from CloudWatch)
3. Flag idle endpoints (no invocations in 7+ days)
4. Display: endpoint table with status, type, age, activity

### Check: Training Jobs

1. List training jobs from last `--days` days
2. For each job:
   - Status (Completed, InProgress, Failed, Stopped)
   - Algorithm, instance type
   - Duration, billable seconds
   - Final metrics (if completed)
3. List active tuning jobs with progress
4. Display: training job table with status, duration, cost

### Check: S3 Buckets

1. List S3 buckets with ML-related prefixes (from `aws_config.json`)
2. For each relevant bucket:
   - Total object count and size
   - Storage class breakdown
   - Last modified date
   - Versioning and encryption status
3. Display: bucket summary table

### Check: Costs

1. Query Cost Explorer for last `--days` days:
   - SageMaker costs (training, endpoint, processing, notebook)
   - S3 costs (storage, requests, transfer)
   - Lambda costs (invocations, duration)
   - Glue costs (ETL, crawlers)
   - Total ML-related spend
2. Compare to previous period (percent change)
3. Display: cost breakdown table with trend

### Final Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-status", {
    "status": "completed",
    "endpoints": endpoint_summary,
    "training_jobs": training_summary,
    "s3_buckets": s3_summary,
    "costs": cost_summary,
    "alerts": [
        {"type": "idle_endpoint", "resource": "...", "recommendation": "..."},
        {"type": "cost_spike", "service": "...", "change_pct": ...}
    ]
})
```

Print full status dashboard: endpoints, jobs, storage, costs, alerts.
