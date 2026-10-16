---
name: prompt-engineering-patterns
description: Design effective prompts for LLM agents with structured input/output formats, chain-of-thought reasoning, few-shot examples, and system prompt architecture. Covers Claude-specific patterns and multi-turn conversation design. Triggers on prompt design, LLM interaction patterns, or system prompt architecture requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - prompt-engineering
  - llm
  - system-prompts
  - chain-of-thought
  - few-shot
governance_phases: [build]
organ_affinity: [all]
triggers: [user-asks-about-prompts, context:prompt-design, context:llm-interaction, context:system-prompt]
complements: [agent-swarm-orchestrator, session-lifecycle-patterns, cross-agent-handoff]
---

# Prompt Engineering Patterns

Design prompts that produce reliable, structured, high-quality outputs from language models.

## Prompt Architecture

### System Prompt Structure

```
┌─ Identity & Role ─────────────────┐
│ Who the model is, what it does     │
├─ Context & Constraints ───────────┤
│ Domain knowledge, guardrails       │
├─ Output Format ───────────────────┤
│ Structure, length, style           │
├─ Examples (Few-Shot) ─────────────┤
│ Input/output pairs                 │
├─ Instructions ────────────────────┤
│ Step-by-step task guidance         │
└────────────────────────────────────┘
```

### Priority Layering

When instructions conflict, models follow this precedence:

1. **System prompt** — Highest structural authority
2. **Most recent user message** — Immediate task context
3. **Earlier conversation** — Background context
4. **Training data** — Default behaviors

## Core Patterns

### Structured Output

```xml
<system>
Analyze the given code and return findings in this exact format:

<analysis>
  <summary>One-sentence overall assessment</summary>
  <findings>
    <finding severity="high|medium|low">
      <location>file:line</location>
      <issue>Description</issue>
      <fix>Recommended fix</fix>
    </finding>
  </findings>
  <score>1-10</score>
</analysis>
</system>
```

### Chain of Thought

```
Before answering, think through the problem step by step:

1. Identify the core question
2. List relevant constraints
3. Consider 2-3 approaches
4. Evaluate tradeoffs
5. Recommend the best approach with reasoning

Show your reasoning in <thinking> tags, then give your final answer.
```

### Few-Shot Examples

```
Classify the following commit messages by type.

Examples:
- "Add user authentication with JWT" → feat
- "Fix null pointer in dashboard render" → fix
- "Update README with API documentation" → docs
- "Refactor database connection pooling" → refactor

Now classify:
- "Implement rate limiting for API endpoints" →
```

### Role Prompting

```
You are a senior security engineer reviewing code for a financial services application.
Your priorities are:
1. Authentication and authorization flaws
2. Data exposure risks
3. Input validation gaps
4. Dependency vulnerabilities

Review with the paranoia appropriate for systems handling financial data.
```

## Advanced Patterns

### Constraint Prompting

```
Generate a Python function with these constraints:
- No external dependencies (stdlib only)
- Must handle the empty input case
- Must include type hints
- Maximum 20 lines
- Must include a docstring
```

### Decomposition

Break complex tasks into sequential sub-prompts:

```
Step 1: Analyze the current code structure
Step 2: Identify the specific change needed
Step 3: Write the minimal diff
Step 4: Verify the change doesn't break existing behavior
```

### Self-Verification

```
After generating your response:
1. Re-read the original question
2. Check that every requirement is addressed
3. Verify any code compiles/runs mentally
4. Flag any assumptions you made
```

### Negative Prompting

Specify what NOT to do:

```
Important:
- Do NOT add error handling beyond what was requested
- Do NOT refactor surrounding code
- Do NOT add comments explaining obvious operations
- Do NOT change the function signature
```

## Claude-Specific Patterns

### XML Tags for Structure

Claude responds well to XML-tagged sections:

```xml
<context>
  Repository: a-i--skills
  Organ: IV (Orchestration)
  Current branch: feature/governance-aware-skill-taxonomy
</context>

<task>
  Create a new skill following the existing frontmatter format.
</task>

<constraints>
  - Match the YAML frontmatter schema exactly
  - Name must match directory name
  - Include governance metadata fields
</constraints>
```

### Extended Thinking

For complex reasoning tasks, allocate thinking budget:

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000,
    },
    messages=[{"role": "user", "content": prompt}],
)
```

### Tool Use

Define tools for structured interaction:

```python
tools = [{
    "name": "create_skill",
    "description": "Create a new skill file",
    "input_schema": {
        "type": "object",
        "required": ["name", "category", "description"],
        "properties": {
            "name": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "category": {"type": "string"},
            "description": {"type": "string", "maxLength": 600},
        },
    },
}]
```

## Multi-Turn Conversation Design

### Context Window Management

```
Conversation budget allocation:
- System prompt: ~2K tokens (fixed)
- Conversation history: ~50K tokens (growing)
- Current task context: ~10K tokens (variable)
- Response space: ~4K tokens (reserved)
```

### Conversation Summarization

When context grows large, summarize earlier turns:

```
<conversation_summary>
In previous messages, we:
1. Identified the bug in auth middleware (missing token refresh)
2. Agreed on fix approach (add refresh check before expiry)
3. Implemented the fix in src/auth/middleware.ts
</conversation_summary>

Now continuing with testing...
```

## Prompt Testing

### Evaluation Criteria

| Criterion | Test Method |
|-----------|-------------|
| Correctness | Compare output against known-good answers |
| Consistency | Run same prompt 5x, check variance |
| Format compliance | Validate output structure programmatically |
| Edge cases | Test with empty input, long input, adversarial input |
| Robustness | Rephrase prompt, check output stability |

### A/B Testing Prompts

```python
async def evaluate_prompts(prompts: list[str], test_cases: list[dict]) -> dict:
    results = {}
    for i, prompt in enumerate(prompts):
        scores = []
        for case in test_cases:
            output = await generate(prompt, case["input"])
            score = evaluate(output, case["expected"])
            scores.append(score)
        results[f"prompt_{i}"] = sum(scores) / len(scores)
    return results
```

## Anti-Patterns

- **Vague instructions** — "Do something good" vs. "Return a JSON object with exactly 3 fields"
- **Conflicting constraints** — "Be concise" + "Explain thoroughly"
- **Prompt injection vulnerability** — Always separate system instructions from user input
- **No output format spec** — Always specify expected format for machine-consumed output
- **Over-prompting** — Adding unnecessary instructions that dilute important ones
- **Ignoring model capabilities** — Using chain-of-thought when a simple instruction suffices
