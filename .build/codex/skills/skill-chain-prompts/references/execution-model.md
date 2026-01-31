# Execution Model

How Claude processes skill chains without an external engine.

## Core Concept

Chains work through Claude's sequential conversation processing. Each step:
1. Invokes a skill using `/skill-name` syntax
2. Tracks completion in conversation state
3. Passes context to subsequent steps
4. Pauses at checkpoints for user review

No external runtime, database, or orchestration engine required.

## Execution Modes

### Sequential (Default)

Steps execute in definition order, respecting dependencies:

```yaml
execution:
  mode: sequential
```

Process:
1. Find next incomplete step with satisfied dependencies
2. Announce: "Starting step: {id} ({skill})"
3. Invoke the skill
4. Mark step complete with notes
5. Update progress display
6. Repeat until chain complete

### Parallel (Conceptual)

Independent steps can be worked on together:

```yaml
execution:
  mode: parallel
```

```
Steps A, B have no dependencies → Can start both
Step C depends on A → Waits for A
Step D depends on A and B → Waits for both
```

In practice, "parallel" means Claude can:
- Work on multiple independent artifacts
- Ask user which step to focus on
- Interleave work between steps

True parallelism requires the multi-agent-workforce-planner skill.

## Step Lifecycle

```
○ Pending     Initial state, waiting for dependencies
    ↓
◐ Active      Currently being worked on
    ↓
● Complete    Successfully finished
    or
✕ Failed      Error occurred, chain paused
    or
⊖ Skipped     Optional step was skipped
```

## Dependency Resolution

Dependencies control execution order:

```yaml
steps:
  - id: a
    skill: skill-one
    # No dependencies, runs first

  - id: b
    skill: skill-two
    depends_on: [a]
    # Runs after a completes

  - id: c
    skill: skill-three
    depends_on: [a]
    # Also runs after a (parallel with b)

  - id: d
    skill: skill-four
    depends_on: [b, c]
    # Waits for both b and c
```

Execution graph:
```
    a
   / \
  b   c
   \ /
    d
```

## Context Passing

Outputs from one step become inputs to later steps:

```yaml
steps:
  - id: design
    skill: api-design-patterns
    outputs: [openapi-spec, endpoints]

  - id: implement
    skill: backend-implementation-patterns
    depends_on: [design]
    inputs: [openapi-spec]  # References design's output
```

Context passed automatically through conversation:
- Artifacts created in earlier steps remain accessible
- Claude references prior work when invoking next skill
- User can view/modify artifacts between steps

## Checkpoints

Checkpoints pause the chain for user review:

```yaml
- id: verify
  skill: verification-loop
  checkpoint: true
```

At checkpoint:
1. Step completes
2. Chain pauses with summary
3. User reviews:
   - Artifacts created
   - Quality of outputs
   - Any issues to address
4. User decides:
   - `/skill-chain-prompts resume` — Continue
   - Redo current step
   - Modify and continue
   - Abort chain

### Checkpoint Summary Format

```markdown
## Checkpoint Reached: verify

**Chain**: api-development
**Completed Steps**: 4/5
**Current Artifacts**:
- openapi-spec.yaml (API contract)
- test-suite/ (42 test files)
- src/api/ (implementation)
- verification-report.md (all tests passing)

**Next Step**: deploy (optional)

Ready to continue? Use `/skill-chain-prompts resume` or `/skill-chain-prompts skip`.
```

## Failure Handling

### on_failure: pause (Default)

```yaml
execution:
  on_failure: pause
```

When step fails:
1. Mark step as ✕ Failed
2. Show error context
3. Wait for user decision:
   - Retry step
   - Fix issue and resume
   - Skip step (if optional)
   - Abort chain

### on_failure: skip

```yaml
execution:
  on_failure: skip
```

When step fails:
1. Mark step as ✕ Failed
2. Continue to next step
3. Dependents proceed without failed step's outputs
4. Summary shows skipped step

### on_failure: abort

```yaml
execution:
  on_failure: abort
```

When step fails:
1. Mark step as ✕ Failed
2. Stop chain immediately
3. Show final state
4. No automatic recovery

## Retries

Steps can specify retry count:

```yaml
- id: flaky-step
  skill: some-skill
  retries: 2  # Try up to 3 times total
```

On failure:
1. First attempt fails
2. Retry attempt 1
3. Retry attempt 2
4. If still failing, apply `on_failure` behavior

## Skill Invocation

Each step invokes its skill using standard syntax:

```
Invoking: /api-design-patterns

[Skill executes normally within conversation]

Step 'design' complete.
Outputs: openapi-spec, endpoint-list
```

The skill has full access to:
- All prior conversation context
- Artifacts from completed steps
- User preferences and instructions

## State Persistence

Chain state exists only in conversation:
- Progress tracked in markdown tables
- Artifacts in conversation history
- No external database

Implications:
- State lost if conversation ends
- Long chains may hit context limits
- Consider breaking into sub-chains

## Tips

1. **Keep chains short** — 3-7 steps work well
2. **Use checkpoints** — Add after significant work
3. **Mark optional steps** — Deployment often optional
4. **Handle failures** — Set appropriate on_failure
5. **Pass context explicitly** — Use outputs/inputs fields
