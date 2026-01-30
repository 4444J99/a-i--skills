# /speckit.plan Command

Creates an implementation plan from an existing feature specification.

## Usage

```
/speckit.plan [tech-context]
```

**Examples**:
- `/speckit.plan` - Determine tech from project context
- `/speckit.plan WebSocket, PostgreSQL, Redis` - Specify tech stack

## Prerequisites

- `spec.md` must exist in the feature directory
- All `[NEEDS CLARIFICATION]` markers should be resolved

## User Input

The text after `/speckit.plan` provides technical context. If empty, determine appropriate technology from:
- Existing project configuration
- Feature requirements
- Research phase findings

## Execution Workflow

### 1. Setup

Identify the feature directory containing `spec.md`:
```
specs/{feature-name}/
├── spec.md          # Input (required)
├── plan.md          # Output (this command)
├── research.md      # Output (Phase 0)
├── data-model.md    # Output (Phase 1)
├── contracts/       # Output (Phase 1)
└── quickstart.md    # Output (Phase 1)
```

### 2. Load Context

1. Read the feature specification (`spec.md`)
2. Load project constitution (`memory/constitution.md`) if exists
3. Load the plan template from `references/plan-template.md`

### 3. Fill Technical Context

Complete the Technical Context section:

```markdown
**Language/Version**: [e.g., Python 3.11]
**Primary Dependencies**: [e.g., FastAPI, SQLAlchemy]
**Storage**: [e.g., PostgreSQL]
**Testing**: [e.g., pytest]
**Target Platform**: [e.g., Linux server]
**Project Type**: [single/web/mobile]
**Performance Goals**: [e.g., 1000 req/s]
**Constraints**: [e.g., <200ms p95]
**Scale/Scope**: [e.g., 10k users]
```

Mark unknowns as `NEEDS CLARIFICATION`.

### 4. Constitution Check (if constitution exists)

Evaluate against constitutional gates:

**Simplicity Gate**:
- [ ] Using ≤3 projects?
- [ ] No future-proofing?

**Anti-Abstraction Gate**:
- [ ] Using framework directly?
- [ ] Single model representation?

**Integration-First Gate**:
- [ ] Contracts defined?
- [ ] Contract tests planned?

ERROR if violations are not justified in Complexity Tracking section.

### 5. Phase 0: Research

For each unknown in Technical Context:

1. Research the technology/approach
2. Document decision, rationale, and alternatives considered

**Output**: `research.md`

```markdown
# Research: [Feature]

## [Decision Topic]

**Decision**: [What was chosen]
**Rationale**: [Why chosen]
**Alternatives Considered**: [What else evaluated]

## [Next Decision Topic]
...
```

All `NEEDS CLARIFICATION` must be resolved.

### 6. Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

#### Generate Data Model

Extract entities from spec → `data-model.md`:
- Entity name, fields, relationships
- Validation rules
- State transitions

#### Generate API Contracts

From functional requirements → `contracts/`:
- Each user action → endpoint
- Use REST/GraphQL patterns
- Output OpenAPI or GraphQL schema

#### Generate Quickstart

Create `quickstart.md` with key validation scenarios:
- How to verify each user story works
- Manual test steps
- Expected outcomes

### 7. Finalize Plan

Complete `plan.md` with:
- Summary (primary requirement + approach)
- Technical Context (filled)
- Constitution Check (if applicable)
- Project Structure (concrete paths)
- Complexity Tracking (if violations justified)

### 8. Re-evaluate Constitution

After design, re-check constitutional compliance.
Document any new justified violations.

### 9. Report Completion

Report:
- Branch name
- Plan file path
- Generated artifacts list
- Next step: `/speckit.tasks`

## Key Rules

- Use absolute paths
- ERROR on gate failures without justification
- ERROR on unresolved clarifications
- Keep plan.md high-level and readable
- Detailed specs go in separate files (data-model.md, contracts/)
