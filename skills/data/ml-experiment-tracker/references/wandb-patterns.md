# Weights & Biases Patterns

## Project Organization

```
wandb/
├── entity/                    # User or team
│   ├── project-classification/
│   │   ├── runs/
│   │   │   ├── abc123/       # Individual experiment
│   │   │   ├── def456/
│   │   │   └── ...
│   │   └── artifacts/        # Datasets, models
│   └── project-detection/
```

## Run Configuration

### Basic Run

```python
import wandb

config = {
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32,
    "architecture": "ResNet50",
    "dataset": "CIFAR-10"
}

run = wandb.init(
    project="image-classification",
    config=config,
    name="resnet50-baseline",
    tags=["baseline", "resnet"],
    notes="Testing ResNet50 as baseline model"
)
```

### Grouping Related Runs

```python
# Group runs for comparison
run = wandb.init(
    project="hyperparameter-search",
    group="learning-rate-sweep",
    job_type="train"
)
```

### Resume Runs

```python
# Resume a crashed run
run = wandb.init(
    project="long-training",
    id="abc123",  # Previous run ID
    resume="must"  # or "allow", "never"
)
```

## Logging Patterns

### Metrics

```python
for epoch in range(epochs):
    train_loss = train_epoch()
    val_loss, val_acc = validate()

    # Log metrics
    wandb.log({
        "epoch": epoch,
        "train/loss": train_loss,
        "val/loss": val_loss,
        "val/accuracy": val_acc
    })

    # Step is auto-incremented, or specify explicitly
    wandb.log({"lr": scheduler.get_last_lr()[0]}, step=epoch)
```

### Media

```python
# Images
wandb.log({"samples": [wandb.Image(img, caption=f"Sample {i}")
                        for i, img in enumerate(images)]})

# Tables
table = wandb.Table(columns=["id", "image", "prediction", "label"])
for item in predictions:
    table.add_data(item.id, wandb.Image(item.image),
                   item.pred, item.label)
wandb.log({"predictions": table})

# Plots
wandb.log({"confusion_matrix": wandb.plot.confusion_matrix(
    probs=None,
    y_true=labels,
    preds=predictions,
    class_names=class_names
)})

# Audio
wandb.log({"audio": wandb.Audio(audio_array, sample_rate=16000)})
```

### Artifacts

```python
# Log dataset as artifact
artifact = wandb.Artifact(
    name="training-data",
    type="dataset",
    description="Preprocessed training dataset"
)
artifact.add_dir("data/processed/")
run.log_artifact(artifact)

# Log model as artifact
model_artifact = wandb.Artifact(
    name="trained-model",
    type="model",
    metadata={"accuracy": 0.95}
)
model_artifact.add_file("model.pt")
run.log_artifact(model_artifact)

# Use artifact in another run
artifact = run.use_artifact("training-data:latest")
data_dir = artifact.download()
```

## Hyperparameter Sweeps

### Sweep Configuration

```yaml
# sweep.yaml
program: train.py
method: bayes
metric:
  name: val/accuracy
  goal: maximize
parameters:
  learning_rate:
    distribution: log_uniform_values
    min: 1e-5
    max: 1e-1
  batch_size:
    values: [16, 32, 64, 128]
  optimizer:
    values: ["adam", "sgd", "adamw"]
  dropout:
    distribution: uniform
    min: 0.1
    max: 0.5
early_terminate:
  type: hyperband
  min_iter: 3
  eta: 3
```

### Running Sweeps

```bash
# Create sweep
wandb sweep sweep.yaml

# Run agent (can run multiple)
wandb agent username/project/sweep_id
```

### Sweep in Code

```python
sweep_config = {
    "method": "bayes",
    "metric": {"name": "val_loss", "goal": "minimize"},
    "parameters": {
        "lr": {"min": 0.0001, "max": 0.1, "distribution": "log_uniform_values"},
        "batch_size": {"values": [16, 32, 64]}
    }
}

sweep_id = wandb.sweep(sweep_config, project="my-project")

def train():
    with wandb.init() as run:
        config = wandb.config
        model = build_model(config.lr)
        # ... training loop

wandb.agent(sweep_id, train, count=50)
```

## Alerts

```python
# Set up alerts in UI or via API
wandb.alert(
    title="Training Complete",
    text=f"Model achieved {accuracy:.2%} accuracy",
    level=wandb.AlertLevel.INFO
)

# Alert on anomaly
if loss > threshold:
    wandb.alert(
        title="High Loss Detected",
        text=f"Loss {loss} exceeded threshold {threshold}",
        level=wandb.AlertLevel.WARN
    )
```
