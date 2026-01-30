# Dataset Formats for Fine-Tuning

Standard data formats and templates for LLM fine-tuning.

## JSONL Format Basics

Each line is a valid JSON object. No trailing commas.

```jsonl
{"instruction": "...", "input": "...", "output": "..."}
{"instruction": "...", "input": "...", "output": "..."}
```

## Common Dataset Formats

### Alpaca Format

Standard instruction-tuning format. Most widely supported.

```json
{
  "instruction": "Summarize the following text.",
  "input": "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.",
  "output": "A pangram sentence featuring a fox jumping over a dog."
}
```

**Without input:**
```json
{
  "instruction": "Write a haiku about programming.",
  "input": "",
  "output": "Code flows like water\nBugs emerge from the shadows\nStack overflow saves"
}
```

### ShareGPT Format

Multi-turn conversation format. Best for chat models.

```json
{
  "conversations": [
    {"from": "human", "value": "What is machine learning?"},
    {"from": "gpt", "value": "Machine learning is a subset of artificial intelligence..."},
    {"from": "human", "value": "Can you give me an example?"},
    {"from": "gpt", "value": "Sure! A common example is email spam filtering..."}
  ]
}
```

**Role variations by platform:**

| Platform | User Role | Assistant Role |
|----------|-----------|----------------|
| ShareGPT | human | gpt |
| OpenAI | user | assistant |
| Anthropic | human | assistant |

### OpenAI Messages Format

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there! How can I help you today?"}
  ]
}
```

### Completion Format

Simple prompt-completion pairs for base model fine-tuning.

```json
{
  "prompt": "Q: What is 2+2?\nA:",
  "completion": " 4"
}
```

## Chat Templates

### Llama 3 / Llama 3.1

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello!<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>
```

### Mistral / Mixtral

```
<s>[INST] You are a helpful assistant.

Hello! [/INST]Hi there!</s>
```

### ChatML (Many models)

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
Hello!<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

### Gemma

```
<start_of_turn>user
Hello!<end_of_turn>
<start_of_turn>model
Hi there!<end_of_turn>
```

## Data Quality Checklist

### Before Training

- [ ] Remove duplicates
- [ ] Check for data leakage (eval data in train)
- [ ] Validate JSON syntax
- [ ] Ensure consistent formatting
- [ ] Balance response lengths
- [ ] Remove low-quality examples
- [ ] Check for PII/sensitive data
- [ ] Verify correct labels/outputs

### Quality Indicators

| Indicator | Good | Bad |
|-----------|------|-----|
| Response length | Varies naturally | All same length |
| Instruction variety | Diverse phrasing | Copy-paste variations |
| Output quality | Clear, complete | Truncated, nonsensical |
| Format consistency | Same structure | Mixed formats |

## Dataset Size Guidelines

| Use Case | Minimum Samples | Recommended |
|----------|-----------------|-------------|
| Style transfer | 50-100 | 200-500 |
| New task | 500-1000 | 2000-5000 |
| Domain adaptation | 1000-5000 | 10000+ |
| General improvement | 5000+ | 50000+ |

**Rule of thumb:** Quality over quantity. 500 excellent examples beat 5000 mediocre ones.

## Conversion Scripts

### CSV to Alpaca JSONL

```python
import csv
import json

def csv_to_alpaca(input_csv, output_jsonl):
    with open(input_csv, 'r') as f_in, open(output_jsonl, 'w') as f_out:
        reader = csv.DictReader(f_in)
        for row in reader:
            example = {
                "instruction": row['instruction'],
                "input": row.get('input', ''),
                "output": row['output']
            }
            f_out.write(json.dumps(example) + '\n')
```

### Alpaca to ShareGPT

```python
import json

def alpaca_to_sharegpt(input_jsonl, output_jsonl):
    with open(input_jsonl, 'r') as f_in, open(output_jsonl, 'w') as f_out:
        for line in f_in:
            alpaca = json.loads(line)

            user_content = alpaca['instruction']
            if alpaca.get('input'):
                user_content += f"\n\n{alpaca['input']}"

            sharegpt = {
                "conversations": [
                    {"from": "human", "value": user_content},
                    {"from": "gpt", "value": alpaca['output']}
                ]
            }
            f_out.write(json.dumps(sharegpt) + '\n')
```

### Text to Completion Format

```python
import json

def text_to_completion(input_txt, output_jsonl, delimiter="###"):
    with open(input_txt, 'r') as f_in, open(output_jsonl, 'w') as f_out:
        text = f_in.read()
        examples = text.split(delimiter)

        for example in examples:
            if '\n\nResponse:' in example:
                prompt, completion = example.split('\n\nResponse:', 1)
                entry = {
                    "prompt": prompt.strip() + "\n\nResponse:",
                    "completion": completion.strip()
                }
                f_out.write(json.dumps(entry) + '\n')
```

## Validation Script

```python
import json
import sys

def validate_jsonl(filepath, format_type='alpaca'):
    errors = []
    valid_count = 0

    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                data = json.loads(line)

                if format_type == 'alpaca':
                    assert 'instruction' in data, "Missing 'instruction'"
                    assert 'output' in data, "Missing 'output'"
                    assert isinstance(data.get('input', ''), str), "'input' must be string"

                elif format_type == 'sharegpt':
                    assert 'conversations' in data, "Missing 'conversations'"
                    assert len(data['conversations']) >= 2, "Need at least 2 turns"
                    for turn in data['conversations']:
                        assert 'from' in turn, "Missing 'from' in turn"
                        assert 'value' in turn, "Missing 'value' in turn"

                valid_count += 1

            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: Invalid JSON - {e}")
            except AssertionError as e:
                errors.append(f"Line {i}: {e}")

    print(f"Valid examples: {valid_count}")
    print(f"Errors: {len(errors)}")
    for error in errors[:10]:
        print(f"  {error}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more errors")

if __name__ == "__main__":
    validate_jsonl(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'alpaca')
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Trailing commas | Invalid JSON | Remove commas before `}` |
| Missing quotes | Invalid JSON | Quote all strings |
| Inconsistent roles | Confuses model | Standardize role names |
| Empty outputs | Teaches nothing | Remove or fill in |
| Very long examples | May truncate | Split or summarize |
| All identical lengths | Unnatural | Vary response lengths |
