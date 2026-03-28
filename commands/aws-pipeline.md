# /aws-pipeline

Build a SageMaker Pipeline with data processing, training, evaluation, and deployment steps.

## Usage

```
/aws-pipeline <data_s3_uri> [--name <pipeline_name>] [--algorithm xgboost|linear|custom] [--target <column>] [--deploy] [--schedule <cron>]
```

- `data_s3_uri`: S3 URI to raw data
- `--name`: pipeline name (default: project name + timestamp)
- `--algorithm`: training algorithm (default: `xgboost`)
- `--target`: target column for supervised learning
- `--deploy`: include deployment step in pipeline
- `--schedule`: cron expression for recurring execution (e.g., `cron(0 8 * * ? *)`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `aws_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/aws_utils.py`
3. Verify AWS credentials and SageMaker Pipelines permissions
4. Verify required packages: `boto3`, `sagemaker`

### Stage 1: Pipeline Design

1. Analyze data and requirements to determine pipeline steps:
   - **Processing Step**: data cleaning, feature engineering, train/test split
   - **Training Step**: model training with selected algorithm
   - **Evaluation Step**: model evaluation on test set
   - **Condition Step**: check if model meets quality threshold
   - **Register Step**: register model in Model Registry (if passes)
   - **Deploy Step**: create/update endpoint (if `--deploy` and passes)
2. Define pipeline parameters:
   - `processing_instance_type`, `training_instance_type`
   - `model_approval_status`, `accuracy_threshold`
3. Report: pipeline architecture diagram (text)

### Stage 2: Processing Step

1. Generate `src/preprocessing.py`:
   - Load raw data from S3
   - Handle missing values, encode categoricals
   - Feature scaling and selection
   - Train/validation/test split
   - Save processed splits to S3
2. Configure SageMaker Processing step:
   - SKLearn or PySpark processor
   - Input/output channels
   - Instance type and count

### Stage 3: Training Step

1. Configure Estimator:
   - Algorithm container, hyperparameters
   - Input channels from processing output
   - Output model artifact path
2. If tuning requested: wrap in HyperparameterTuner step
3. Configure metric definitions for tracking

### Stage 4: Evaluation Step

1. Generate `src/evaluate.py`:
   - Load model and test data
   - Run predictions
   - Compute metrics (task-appropriate)
   - Write evaluation report JSON to S3
2. Configure Processing step for evaluation
3. Define quality gate condition:
   - Parse evaluation report
   - Check metrics against thresholds
   - Branch: pass -> register/deploy, fail -> stop

### Stage 5: Registration and Deployment Steps

1. **Model Registry Step**:
   - Create model package with inference spec
   - Attach evaluation metrics as metadata
   - Set approval status
2. **Deployment Step** (if `--deploy`):
   - Create/update SageMaker endpoint
   - Configure autoscaling

### Stage 6: Pipeline Assembly

1. Generate `src/pipeline.py` assembling all steps
2. Create pipeline with SageMaker SDK
3. Upsert pipeline definition
4. If `--schedule`: create EventBridge rule for recurring execution
5. Execute pipeline (first run)
6. Report: pipeline ARN, execution ARN, step status

### Stage 7: Report

```python
from ml_utils import save_agent_report
save_agent_report("aws-ml-engineer", {
    "status": "completed",
    "pipeline_name": pipeline_name,
    "pipeline_arn": pipeline_arn,
    "steps": step_summary,
    "execution_arn": execution_arn,
    "schedule": schedule_expression,
    "generated_files": ["src/preprocessing.py", "src/evaluate.py", "src/pipeline.py"],
    "recommendations": recommendations
})
```

Print pipeline summary: steps, parameters, schedule, generated files.
