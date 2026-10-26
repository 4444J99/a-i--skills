# Chain Format Specification

Complete YAML specification for defining skill chains.

## Root Structure

```yaml
chain:
  name: string          # Required: chain identifier (lowercase, hyphens)
  description: string   # Required: what chain accomplishes
  version: string       # Optional: semantic version (default: "1.0.0")

steps:
  - <step definition>   # Required: at least one step

execution:
  mode: string          # Optional: "sequential" (default) or "parallel"
  on_failure: string    # Optional: "pause" (default), "skip", or "abort"
  timeout: string       # Optional: per-step timeout (e.g., "30m")
```

## Step Definition

```yaml
- id: string            # Required: unique step identifier
  skill: string         # Required: skill name to invoke
  description: string   # Optional: what this step accomplishes

  # Dependencies
  depends_on: [string]  # Optional: step IDs that must complete first

  # Outputs
  outputs: [string]     # Optional: artifacts this step produces
  inputs: [string]      # Optional: required inputs from prior steps

  # Control Flow
  checkpoint: boolean   # Optional: pause after this step (default: false)
  optional: boolean     # Optional: can be skipped (default: false)
  retries: integer      # Optional: retry count on failure (default: 0)

  # Customization
  args: string          # Optional: arguments to pass to skill
  context: string       # Optional: additional context for the step
```

## Complete Example

```yaml
chain:
  name: "api-development"
  description: "Full API development from design to deployment"
  version: "1.0.0"

steps:
  - id: design
    skill: api-design-patterns
    description: "Design API structure, endpoints, and contracts"
    outputs: [openapi-spec, endpoint-list, data-models]
    context: "Focus on RESTful design with clear resource naming"

  - id: test-first
    skill: tdd-workflow
    description: "Write tests before implementation"
    depends_on: [design]
    inputs: [endpoint-list]
    outputs: [test-suite]

  - id: implement
    skill: backend-implementation-patterns
    description: "Implement API endpoints"
    depends_on: [test-first]
    inputs: [openapi-spec, test-suite]
    outputs: [source-code]
    retries: 1

  - id: verify
    skill: verification-loop
    description: "Verify implementation meets requirements"
    depends_on: [implement]
    checkpoint: true
    outputs: [verification-report]

  - id: deploy
    skill: deployment-cicd
    description: "Deploy to staging/production"
    depends_on: [verify]
    optional: true
    args: "--environment staging"

execution:
  mode: sequential
  on_failure: pause
  timeout: "60m"
```

## Field Details

### chain.name
- Lowercase letters, numbers, and hyphens only
- Must be unique within your chain collection
- Used for `/skill-chain-prompts run <name>`

### chain.description
- One sentence describing the workflow's goal
- Shown when listing or starting chains

### step.id
- Unique within the chain
- Used in `depends_on` references
- Lowercase, underscores allowed

### step.skill
- Must match a skill's `name` frontmatter exactly
- Chain validation checks skill exists

### step.depends_on
- Array of step IDs that must complete first
- Creates execution order for parallel mode
- Circular dependencies are invalid

### step.outputs
- Named artifacts this step produces
- Referenced by later steps via `inputs`
- Used for context passing

### step.checkpoint
- When `true`, chain pauses after step completes
- User must `/skill-chain-prompts resume` to continue
- Good for review points

### step.optional
- When `true`, step can be skipped with `/skill-chain-prompts skip`
- Shows as ⊖ in progress display
- Dependents still run (they just won't get this step's outputs)

### execution.mode
- `sequential`: Steps run one at a time in order
- `parallel`: Independent steps can run concurrently

### execution.on_failure
- `pause`: Stop and wait for user decision
- `skip`: Mark failed, continue to next step
- `abort`: Stop entire chain immediately

## Validation Rules

1. Every step must have unique `id`
2. `depends_on` must reference valid step IDs
3. No circular dependencies allowed
4. `skill` must reference existing skill name
5. Chain must have at least one step

## Minimal Chain

Simplest valid chain:

```yaml
chain:
  name: "simple"
  description: "Single step chain"

steps:
  - id: only
    skill: some-skill
```
