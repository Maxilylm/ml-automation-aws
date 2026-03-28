# /aws-train

Train a model on SageMaker with built-in algorithms, custom containers, or hyperparameter tuning.

## Usage

```
/aws-train <data_s3_uri> [--algorithm xgboost|linear|image-classification|custom] [--image <ecr_uri>] [--instance ml.m5.xlarge] [--count 1] [--spot] [--tune] [--max-jobs 20]
```

- `data_s3_uri`: S3 URI to training data (or local path to upload first)
- `--algorithm`: built-in SageMaker algorithm (default: `xgboost`)
- `--image`: custom ECR container image URI (overrides `--algorithm`)
- `--instance`: training instance type (default: `ml.m5.xlarge`)
- `--count`: number of training instances (default: 1)
- `--spot`: use managed spot training (up to 90% cost savings)
- `--tune`: enable hyperparameter tuning instead of single training job
- `--max-jobs`: max tuning jobs when `--tune` is set (default: 20)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Verify AWS credentials and SageMaker permissions
4. Verify `boto3` and `sagemaker` SDK installed

### Stage 1: Data Preparation

1. If local path provided: upload to S3 with progress bar
2. Validate S3 data:
   - Check file format (CSV, LibSVM, RecordIO, Parquet)
   - Verify channel structure (train/, validation/ subdirectories)
   - Report: row count, column count, file sizes
3. If data not already split: split 80/20 and upload both channels

### Stage 2: Training Configuration

1. **Built-in algorithm**:
   - Resolve container image URI for region
   - Set algorithm-specific hyperparameters:
     - XGBoost: `max_depth=6`, `eta=0.3`, `objective`, `num_round=100`
     - Linear Learner: `predictor_type`, `mini_batch_size`
     - Image Classification: `num_classes`, `num_training_samples`, `epochs`
   - Configure content type and input mode
2. **Custom container**:
   - Verify ECR image exists and is accessible
   - Set entry point and hyperparameters from project config
3. Configure instance(s), spot training, max runtime, output path
4. Report: full training configuration summary

### Stage 3: Training Execution

1. If `--tune` flag:
   - Define hyperparameter ranges (continuous, integer, categorical)
   - Set objective metric and strategy (Bayesian)
   - Launch tuning job
   - Monitor: best objective value, completed/running/failed jobs
   - Report: best hyperparameters, best metrics, tuning job ARN
2. If single training:
   - Launch training job
   - Stream CloudWatch logs in real-time
   - Track metrics from log output
   - Report: training job ARN, duration, final metrics

### Stage 4: Model Artifact

1. Download model artifact summary from S3
2. Register in SageMaker Model Registry (optional, prompt user)
3. Report: model artifact S3 URI, model size, registry ARN

### Stage 5: Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-ml-engineer", {
    "status": "completed",
    "algorithm": algorithm,
    "instance_type": instance_type,
    "spot": spot_enabled,
    "training_job_arn": job_arn,
    "duration_minutes": duration,
    "metrics": final_metrics,
    "model_artifact": model_s3_uri,
    "cost": {"instance_hours": hours, "estimated_cost": cost},
    "tuning": tuning_summary if tuned else None
})
```

Print training summary: algorithm, instance, duration, metrics, cost, model location.
