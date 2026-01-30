# Fine-Tuning Hyperparameter Guide

Practical settings for LoRA/QLoRA fine-tuning on consumer hardware.

## Quick Start Configurations

### Small Dataset (< 500 examples)

```yaml
# Conservative settings to prevent overfitting
learning_rate: 1e-4
num_epochs: 3
batch_size: 4
gradient_accumulation_steps: 4
lora_r: 8
lora_alpha: 16
lora_dropout: 0.1
warmup_ratio: 0.1
```

### Medium Dataset (500-5000 examples)

```yaml
learning_rate: 2e-4
num_epochs: 2
batch_size: 4
gradient_accumulation_steps: 4
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
warmup_ratio: 0.03
```

### Large Dataset (> 5000 examples)

```yaml
learning_rate: 2e-4
num_epochs: 1
batch_size: 8
gradient_accumulation_steps: 2
lora_r: 32
lora_alpha: 64
lora_dropout: 0.05
warmup_ratio: 0.03
```

## LoRA Parameters

### Rank (r)

Controls the expressiveness of the adaptation.

| Rank | Use Case | VRAM Impact |
|------|----------|-------------|
| 4 | Minor style changes | Minimal |
| 8 | Standard fine-tuning | Low |
| 16 | Complex tasks | Moderate |
| 32 | Domain adaptation | Higher |
| 64+ | Near full fine-tuning | Significant |

**Rule of thumb:** Start with r=8, increase if underfitting.

### Alpha (lora_alpha)

Scaling factor for LoRA weights. Common patterns:

```
alpha = 2 * r    # Standard ratio
alpha = r        # More conservative
alpha = 4 * r    # More aggressive
```

**Effective scaling:** `alpha / r` determines update magnitude.

### Target Modules

Which layers to adapt:

| Target | Description | Recommendation |
|--------|-------------|----------------|
| q_proj, v_proj | Attention queries/values | Minimum for most tasks |
| k_proj | Attention keys | Add for complex tasks |
| o_proj | Attention output | Improves expressiveness |
| gate_proj, up_proj, down_proj | MLP layers | Full adaptation |

**Llama/Mistral common targets:**
```python
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj",
                  "gate_proj", "up_proj", "down_proj"]
```

### Dropout

Prevents overfitting on small datasets.

| Dataset Size | Recommended Dropout |
|--------------|---------------------|
| < 100 | 0.1 - 0.2 |
| 100 - 1000 | 0.05 - 0.1 |
| > 1000 | 0.0 - 0.05 |

## Learning Rate

### Starting Points

| Model Size | LoRA LR | Full Fine-tune LR |
|------------|---------|-------------------|
| 7B | 1e-4 to 3e-4 | 1e-5 to 5e-5 |
| 13B | 1e-4 to 2e-4 | 5e-6 to 2e-5 |
| 70B | 5e-5 to 1e-4 | 1e-6 to 1e-5 |

### Scheduler Options

| Scheduler | Behavior | Best For |
|-----------|----------|----------|
| cosine | Smooth decay to near-zero | Most cases |
| linear | Constant decay rate | Short training |
| constant | No decay | Very short runs |
| cosine_with_restarts | Periodic resets | Long training |

## Batch Size and Accumulation

### Effective Batch Size

```
Effective Batch = batch_size * gradient_accumulation_steps * num_gpus
```

| Dataset Size | Recommended Effective Batch |
|--------------|----------------------------|
| < 500 | 8 - 16 |
| 500 - 5000 | 16 - 32 |
| > 5000 | 32 - 64 |

### VRAM Trade-offs

| batch_size | grad_accum | VRAM | Speed |
|------------|------------|------|-------|
| 1 | 16 | Lowest | Slowest |
| 2 | 8 | Low | Slow |
| 4 | 4 | Medium | Medium |
| 8 | 2 | Higher | Fast |

## VRAM Requirements

### Approximate VRAM by Model Size (QLoRA)

| Model | 4-bit | 8-bit | 16-bit |
|-------|-------|-------|--------|
| 7B | 6-8 GB | 10-12 GB | 16-20 GB |
| 13B | 10-12 GB | 18-22 GB | 30-36 GB |
| 34B | 22-26 GB | 40-48 GB | 70+ GB |
| 70B | 40-48 GB | 80+ GB | 140+ GB |

### Reducing VRAM Usage

1. **Enable gradient checkpointing**
   ```python
   gradient_checkpointing=True
   ```

2. **Reduce batch size, increase accumulation**

3. **Use 4-bit quantization (QLoRA)**
   ```python
   load_in_4bit=True
   bnb_4bit_compute_dtype=torch.bfloat16
   ```

4. **Reduce sequence length**
   ```python
   max_seq_length=512  # Instead of 2048
   ```

5. **Target fewer modules**

## Training Duration

### Epochs vs Steps

| Scenario | Epochs | Why |
|----------|--------|-----|
| Small data (< 500) | 3-5 | Need multiple passes |
| Medium data | 2-3 | Balance coverage and overfitting |
| Large data (> 5000) | 1-2 | Single pass often sufficient |

### Overfitting Signs

- Training loss keeps decreasing
- Validation loss starts increasing
- Model outputs become repetitive
- Model memorizes training examples

### Early Stopping

```python
# Save checkpoint when validation loss improves
early_stopping_patience = 3  # Stop after 3 evals without improvement
```

## Quantization Settings

### QLoRA Configuration

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # Normalized float 4
    bnb_4bit_compute_dtype=torch.bfloat16,# Compute precision
    bnb_4bit_use_double_quant=True        # Quantize the quantization
)
```

### Quantization Types

| Type | Description | Recommendation |
|------|-------------|----------------|
| nf4 | Normalized float 4 | Best for most cases |
| fp4 | Standard float 4 | Fallback option |

## Common Issues and Fixes

### Loss Not Decreasing

| Cause | Fix |
|-------|-----|
| LR too low | Increase learning rate |
| Rank too low | Increase LoRA rank |
| Bad data | Check data quality |
| Wrong format | Verify chat template |

### Loss Explodes (NaN)

| Cause | Fix |
|-------|-----|
| LR too high | Reduce learning rate |
| No warmup | Add warmup steps |
| Mixed precision issue | Try different dtype |

### Model Outputs Garbage

| Cause | Fix |
|-------|-----|
| Wrong chat template | Match base model format |
| EOS token issue | Verify tokenizer config |
| Severe overfitting | Reduce epochs, add dropout |

### Out of Memory

| Cause | Fix |
|-------|-----|
| Batch too large | Reduce batch, increase accum |
| Sequence too long | Reduce max_seq_length |
| Too many target modules | Reduce targets |

## Sample Configurations

### Unsloth (Fast Single GPU)

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3-8b-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
)
```

### Axolotl Config

```yaml
base_model: meta-llama/Meta-Llama-3-8B
model_type: LlamaForCausalLM
load_in_4bit: true

adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj

dataset_prepared_path: ./prepared_data
datasets:
  - path: ./data/train.jsonl
    type: alpaca

sequence_len: 2048
micro_batch_size: 2
gradient_accumulation_steps: 8
num_epochs: 2
learning_rate: 2e-4
lr_scheduler: cosine
warmup_ratio: 0.03
```

### Transformers + PEFT

```python
from transformers import TrainingArguments
from peft import LoraConfig

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
)

training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=2,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=10,
    save_strategy="epoch",
    bf16=True,
)
```
