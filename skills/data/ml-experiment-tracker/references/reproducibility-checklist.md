# Reproducibility Checklist

## Code Reproducibility

- [ ] **Version control**: All code in git
- [ ] **Commit hash logged**: Record exact commit for each experiment
- [ ] **Dependencies locked**: `requirements.txt` or `poetry.lock` committed
- [ ] **No uncommitted changes**: Check `git status` before runs

```python
import subprocess

def get_git_info():
    return {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"]
        ).decode().strip(),
        "branch": subprocess.check_output(
            ["git", "branch", "--show-current"]
        ).decode().strip(),
        "dirty": bool(subprocess.check_output(
            ["git", "status", "--porcelain"]
        ).decode().strip())
    }
```

## Environment Reproducibility

- [ ] **Python version**: Specify exact version (3.10.8, not 3.10)
- [ ] **Package versions**: Pin all dependencies
- [ ] **System packages**: Document CUDA, cuDNN versions
- [ ] **Hardware**: Log GPU model, CPU, memory

```python
def log_environment():
    import platform
    import torch

    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "cpu_count": os.cpu_count()
    }
```

## Data Reproducibility

- [ ] **Dataset version**: Hash or version identifier
- [ ] **Preprocessing logged**: All transformations documented
- [ ] **Train/val/test splits**: Seeds and method saved
- [ ] **Data augmentation**: All transforms with parameters

```python
import hashlib

def get_data_hash(filepath):
    """Generate hash for dataset file"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def log_data_split(train_idx, val_idx, test_idx, seed):
    """Log data split for reproducibility"""
    return {
        "split_seed": seed,
        "train_size": len(train_idx),
        "val_size": len(val_idx),
        "test_size": len(test_idx),
        "train_idx_hash": hashlib.md5(str(train_idx).encode()).hexdigest()[:8]
    }
```

## Training Reproducibility

- [ ] **Random seeds set**: Python, NumPy, PyTorch/TensorFlow
- [ ] **All hyperparameters logged**: Including defaults
- [ ] **Checkpoints saved**: At regular intervals
- [ ] **Non-determinism documented**: List any random ops

```python
import random
import numpy as np
import torch

def set_seeds(seed=42):
    """Set all random seeds for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # For fully deterministic behavior (slower)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    return seed
```

## Configuration Template

```yaml
# experiment_config.yaml
experiment:
  name: "baseline-v1"
  seed: 42
  description: "Initial baseline model"

environment:
  python: "3.10.8"
  cuda: "11.8"
  requirements: "requirements.txt"

data:
  dataset: "imagenet"
  version: "2024-01"
  train_split: 0.8
  val_split: 0.1
  test_split: 0.1
  augmentation:
    - name: RandomHorizontalFlip
      p: 0.5
    - name: RandomRotation
      degrees: 15

model:
  architecture: "resnet50"
  pretrained: true
  num_classes: 1000

training:
  epochs: 100
  batch_size: 32
  optimizer:
    name: "adam"
    lr: 0.001
    weight_decay: 0.0001
  scheduler:
    name: "cosine"
    T_max: 100
  loss: "cross_entropy"

checkpoint:
  save_every: 10
  keep_last: 3
```

## Verification Steps

1. **Fresh environment test**: Clone repo, install deps, run training
2. **Seed verification**: Run twice with same seed, compare metrics
3. **Checkpoint restoration**: Load checkpoint, verify same results
4. **Documentation review**: Can someone else reproduce from docs alone?
