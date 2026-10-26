# MLflow Setup Guide

## Installation

```bash
# Basic installation
pip install mlflow

# With specific backends
pip install mlflow[extras]  # All optional dependencies
pip install mlflow psycopg2-binary  # PostgreSQL backend
pip install mlflow boto3  # S3 artifact storage
```

## Server Configuration

### Local Development

```bash
# Simple local server
mlflow ui --port 5000

# With backend store (SQLite)
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlruns \
    --port 5000
```

### Production Setup

```bash
# PostgreSQL backend + S3 artifacts
mlflow server \
    --backend-store-uri postgresql://user:pass@localhost:5432/mlflow \
    --default-artifact-root s3://mlflow-artifacts/experiments \
    --host 0.0.0.0 \
    --port 5000
```

### Docker Compose

```yaml
version: '3'
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_BACKEND_STORE_URI=postgresql://mlflow:mlflow@db:5432/mlflow
      - MLFLOW_DEFAULT_ARTIFACT_ROOT=s3://mlflow-artifacts
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    command: >
      mlflow server
      --backend-store-uri postgresql://mlflow:mlflow@db:5432/mlflow
      --default-artifact-root s3://mlflow-artifacts
      --host 0.0.0.0
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=mlflow
      - POSTGRES_PASSWORD=mlflow
      - POSTGRES_DB=mlflow
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Client Configuration

```python
import mlflow

# Set tracking URI
mlflow.set_tracking_uri("http://mlflow-server:5000")

# Or via environment variable
# export MLFLOW_TRACKING_URI=http://mlflow-server:5000

# Create or set experiment
mlflow.set_experiment("my-experiment")

# Optional: Set tags for the experiment
mlflow.set_experiment_tag("team", "ml-platform")
```

## Model Registry

### Register a Model

```python
# Option 1: Log and register in one step
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="my-classifier"
)

# Option 2: Register existing run's model
result = mlflow.register_model(
    "runs:/abc123/model",
    "my-classifier"
)
```

### Model Stages

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Transition to staging
client.transition_model_version_stage(
    name="my-classifier",
    version=1,
    stage="Staging"
)

# Transition to production
client.transition_model_version_stage(
    name="my-classifier",
    version=1,
    stage="Production"
)
```

### Load Model by Stage

```python
# Load production model
model = mlflow.pyfunc.load_model(
    model_uri="models:/my-classifier/Production"
)

# Load specific version
model = mlflow.pyfunc.load_model(
    model_uri="models:/my-classifier/1"
)
```

## Autologging

```python
# Enable autologging for specific framework
mlflow.sklearn.autolog()
mlflow.pytorch.autolog()
mlflow.tensorflow.autolog()
mlflow.xgboost.autolog()

# Or enable for all supported frameworks
mlflow.autolog()
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MLFLOW_TRACKING_URI` | Tracking server URL |
| `MLFLOW_EXPERIMENT_NAME` | Default experiment |
| `MLFLOW_S3_ENDPOINT_URL` | S3-compatible endpoint |
| `AWS_ACCESS_KEY_ID` | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials |
