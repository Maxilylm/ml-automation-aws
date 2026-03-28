# /aws-coldstart

Full AWS ML workflow from data upload through training to deployment.

## Usage

```
/aws-coldstart <data_path> [--algorithm xgboost|linear|custom] [--target <column>] [--deploy endpoint|lambda|ecs] [--instance ml.m5.xlarge]
```

- `data_path`: path to training data (CSV, Parquet, or S3 URI)
- `--algorithm`: training algorithm (default: `xgboost`)
- `--target`: target column for supervised learning
- `--deploy`: deployment target (default: `endpoint`)
- `--instance`: SageMaker instance type (default: `ml.m5.xlarge`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Verify AWS credentials (`aws_config.json` or environment) -- if missing, run `/aws-connect` logic
4. Verify required packages: `boto3`, `sagemaker`, `pandas`

### Stage 1: Data Upload to S3

1. If `data_path` is local:
   - Validate data format and schema
   - Split into train/validation/test (70/15/15)
   - Upload splits to `s3://<bucket>/data/<project>/train/`, `validation/`, `test/`
2. If `data_path` is S3 URI:
   - Verify access and inspect schema
   - Check if already split; split if needed
3. Report: S3 URIs, row counts per split, column schema

### Stage 2: SageMaker Training

1. Configure training job:
   - Select algorithm container (built-in or custom ECR)
   - Set hyperparameters (algorithm-specific defaults)
   - Configure instance type and count
   - Set input data channels (train, validation)
   - Set output path for model artifacts
2. Launch training job via SageMaker API
3. Monitor training: stream logs, track metrics
4. Report: training job ARN, duration, final metrics, model artifact S3 URI

### Stage 3: Model Evaluation

1. Download test data from S3
2. Create batch transform job on test set
3. Compute evaluation metrics:
   - Classification: accuracy, precision, recall, F1, AUC-ROC
   - Regression: RMSE, MAE, R-squared
4. Report: metrics table, confusion matrix (if classification)

### Stage 4: Model Registration

1. Register model in SageMaker Model Registry
2. Set approval status to `PendingManualApproval`
3. Attach metadata: training job ARN, metrics, data lineage
4. Report: model package ARN, version number

### Stage 5: Deployment

1. Based on `--deploy` flag:
   - **endpoint**: Create real-time SageMaker endpoint with autoscaling
   - **lambda**: Package model into Lambda function with API Gateway
   - **ecs**: Build Docker image, push to ECR, deploy to ECS Fargate
2. Run smoke test against deployed endpoint
3. Report: endpoint URL/ARN, latency, deployment configuration

### Stage 6: Cost Summary

1. Calculate training cost (instance hours x price)
2. Estimate monthly inference cost based on deployment type
3. Suggest cost optimizations (spot training, serverless, reserved)

### Stage 7: Final Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-coldstart", {
    "status": "completed",
    "data": {"s3_uri": data_uri, "train_rows": n_train, "test_rows": n_test},
    "training": {"job_arn": job_arn, "duration_min": duration, "metrics": metrics},
    "model": {"artifact_uri": model_uri, "registry_arn": registry_arn},
    "deployment": {"type": deploy_type, "endpoint": endpoint_url, "latency_p50": p50},
    "cost": {"training": training_cost, "monthly_inference": monthly_cost},
    "recommendations": recommendations
})
```

Print end-to-end summary: data, training, evaluation, deployment, cost.
