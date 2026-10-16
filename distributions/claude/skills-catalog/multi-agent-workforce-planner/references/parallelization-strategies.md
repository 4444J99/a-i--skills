# Parallelization Strategies

Techniques for maximizing parallel work across agent workstreams.

## Strategy Overview

| Strategy | Best For | Speedup Potential |
|----------|----------|-------------------|
| Horizontal | Independent features | High |
| Vertical | Layered architectures | Medium-High |
| Interface-First | Coupled components | Medium |
| Speculative | Predictable work | Variable |
| Pipeline | Sequential processing | Medium |

## Horizontal Parallelization

Run independent features simultaneously.

### Pattern

```
Time →
Feature A: ████████████████████████
Feature B: ████████████████████████
Feature C: ████████████████████████
```

### When to Use

- Multiple unrelated features
- Different domains/modules
- Separate codebases or areas

### Implementation

```yaml
workstreams:
  - name: "User Profile"
    independent: true
    tasks: [U1, U2, U3]

  - name: "Payment System"
    independent: true
    tasks: [P1, P2, P3]

  - name: "Notification Service"
    independent: true
    tasks: [N1, N2, N3]

execution:
  parallel_groups:
    - [User Profile, Payment System, Notification Service]
```

### Considerations

- No shared state between workstreams
- Each workstream has complete ownership
- Integration happens at end

## Vertical Parallelization

Work on different layers simultaneously.

### Pattern

```
Time →
Frontend:  ████████████████
Backend:   ████████████████
Database:  ████████████████
Tests:     ████████████████
```

### When to Use

- Full-stack features
- Layered architecture
- Well-defined interfaces between layers

### Implementation

```yaml
layers:
  - name: "API Layer"
    tasks:
      - "Define REST endpoints"
      - "Implement controllers"
      - "Add validation"

  - name: "Service Layer"
    tasks:
      - "Define service interfaces"
      - "Implement business logic"
      - "Add caching"

  - name: "Data Layer"
    tasks:
      - "Define models"
      - "Implement repositories"
      - "Add migrations"

parallel_execution:
  # All layers can start once interfaces defined
  phase1: [define_all_interfaces]
  phase2: [API Layer, Service Layer, Data Layer]  # Parallel
  phase3: [integration_tests]
```

### Considerations

- Requires clear interface contracts
- Each layer must be testable in isolation
- May need mocks for layer boundaries

## Interface-First Parallelization

Define contracts, then implement in parallel.

### Pattern

```
Time →
Interface: ████
Producer:       ████████████████
Consumer:       ████████████████
Integration:                    ████
```

### When to Use

- Tightly coupled components
- API producer/consumer scenarios
- Microservice communication

### Implementation

```yaml
phases:
  - name: "Contract Phase"
    blocking: true
    tasks:
      - id: C1
        name: "Define API schema"
        agent: Plan
        outputs:
          - api_schema.yaml
          - types.ts

  - name: "Implementation Phase"
    parallel: true
    tasks:
      - id: I1
        name: "Implement API server"
        agent: Edit
        uses: [api_schema.yaml]

      - id: I2
        name: "Implement API client"
        agent: Edit
        uses: [types.ts]

  - name: "Integration Phase"
    tasks:
      - id: T1
        name: "Integration tests"
        agent: Edit
        depends_on: [I1, I2]
```

### Contract Types

```yaml
contracts:
  - type: "OpenAPI"
    path: "api/openapi.yaml"

  - type: "TypeScript Types"
    path: "shared/types.ts"

  - type: "GraphQL Schema"
    path: "schema.graphql"

  - type: "Protocol Buffers"
    path: "proto/service.proto"
```

## Speculative Parallelization

Start work that's likely needed before it's required.

### Pattern

```
Time →
Main:        ████████████████████████
Speculative:     ████████████  (may be discarded)
```

### When to Use

- High-confidence future work
- Long-running preparations
- Test fixture creation

### Implementation

```yaml
main_path:
  - id: M1
    name: "Implement authentication"
    agent: Edit

speculative_work:
  - id: S1
    name: "Create test fixtures"
    agent: Edit
    confidence: 0.95  # Very likely needed
    start_with: [M1]  # Start in parallel

  - id: S2
    name: "Draft documentation"
    agent: Edit
    confidence: 0.70  # Might need changes
    start_with: [M1]

  - id: S3
    name: "Prepare deployment config"
    agent: Edit
    confidence: 0.50  # Only if we deploy today
    start_after: M1  # Wait for more info
```

### Risk Management

```yaml
speculative_policy:
  max_parallel: 2  # Limit wasted work
  abort_on:
    - main_path_failure
    - requirement_change

  on_completion:
    validate_still_needed: true
    may_require_updates: true
```

## Pipeline Parallelization

Overlap sequential stages.

### Pattern

```
Time →
Item 1: ████████████
Item 2:     ████████████
Item 3:         ████████████
Item 4:             ████████████
```

### When to Use

- Batch processing
- Multiple similar items
- Stages with clear handoffs

### Implementation

```yaml
pipeline:
  stages:
    - name: "Analysis"
      agent: Explore
      duration: 1 unit

    - name: "Design"
      agent: Plan
      duration: 1 unit

    - name: "Implementation"
      agent: Edit
      duration: 2 units

    - name: "Testing"
      agent: Bash
      duration: 1 unit

items:
  - Component A
  - Component B
  - Component C
  - Component D

# Pipeline timing:
# Time:    1    2    3    4    5    6    7
# Item A: [An ][De ][Impl    ][Te ]
# Item B:      [An ][De ][Impl    ][Te ]
# Item C:           [An ][De ][Impl    ][Te ]
# Item D:                [An ][De ][Impl    ][Te ]
```

## Combining Strategies

### Real-World Example

```yaml
feature: "E-commerce Checkout"

# Horizontal: Independent domains
horizontal_streams:
  - "Cart Management"
  - "Payment Processing"
  - "Order Confirmation"

# Vertical: Each domain has layers
vertical_layers:
  Cart Management:
    - UI Components
    - Cart Service
    - Cart Storage

# Interface-First: Service contracts
interfaces:
  - "Cart API Contract"
  - "Payment Gateway Contract"
  - "Notification Contract"

# Speculative: Likely needed
speculative:
  - "Email templates"
  - "Error pages"

# Pipeline: Multiple payment methods
pipeline:
  - "Credit Card handler"
  - "PayPal handler"
  - "Bank Transfer handler"
```

## Optimization Tips

### Minimize Critical Path

```
Before: T1 → T2 → T3 → T4 → T5 (5 units)

After:  T1 → T2 ─────┐
              ├──────→ T5 (3 units)
        T3 → T4 ─────┘
```

### Balance Workloads

```yaml
# Bad: Unbalanced
workstream_a: [10 tasks]
workstream_b: [2 tasks]

# Good: Balanced
workstream_a: [6 tasks]
workstream_b: [6 tasks]
```

### Identify Bottlenecks

```
Agent utilization:
Explore: ██████░░░░ 60%
Plan:    ████░░░░░░ 40%
Edit:    ██████████ 100% ← Bottleneck!
Bash:    ██░░░░░░░░ 20%
```

## Anti-Patterns

### Over-Parallelization

```yaml
# Bad: Too fine-grained
- "Write line 1"
- "Write line 2"
- "Write line 3"

# Good: Appropriate granularity
- "Implement function"
```

### Hidden Dependencies

```yaml
# Bad: Undeclared dependency
- id: T1
  name: "Create user"
  # Actually needs database schema from T0!

# Good: Explicit dependency
- id: T1
  name: "Create user"
  depends_on: [T0]
  reason: "Needs users table from migration"
```

### Ignoring Integration

```yaml
# Bad: Only parallel implementation
phases:
  - parallel: [A, B, C, D, E]

# Good: Account for integration
phases:
  - parallel: [A, B, C, D, E]
  - integration: [combine_all]
  - verification: [end_to_end_tests]
```
