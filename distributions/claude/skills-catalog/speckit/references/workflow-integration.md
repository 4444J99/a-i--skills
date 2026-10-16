# Workflow Integration: SpecKit

This document describes how `speckit` integrates with other skills in the development ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `product-requirements-designer` | **Upstream** | Generate PRD before specifying features |
| `tdd-workflow` | **Downstream** | Apply TDD after task generation |
| `verification-loop` | **Downstream** | Verify implementation against spec |
| `backend-implementation-patterns` | **Downstream** | Implement API contracts from plan |
| `api-design-patterns` | **Complementary** | Inform contract design during planning |
| `testing-patterns` | **Complementary** | Guide test strategy in tasks |
| `skill-chain-prompts` | **Orchestrator** | Chain speckit commands with other skills |
| `github-repository-standards` | **Complementary** | Structure repo around generated specs |

## Prerequisites

Before invoking `speckit`, ensure:

1. **Feature idea exists** - A clear description of what to build
2. **Project context available** - Existing codebase or greenfield decision made
3. **Stakeholder alignment** - Agreement on scope and priorities

## Handoff Patterns

### From: product-requirements-designer

**Trigger:** PRD completed with defined features.

**What speckit receives:**
- Feature descriptions from the PRD
- User personas and journeys
- Success metrics
- Business constraints

**SpecKit action:** Run `/speckit.specify` for each feature in the PRD.

### To: tdd-workflow

**Trigger:** `/speckit.tasks` completed with task list.

**What to hand off:**
- Task list with test markers
- Acceptance criteria from spec.md
- API contracts from contracts/
- Data models from data-model.md

**Expected output from TDD:**
- Red-green-refactor cycle per task
- Contract tests passing
- Integration tests passing

### To: verification-loop

**Trigger:** Implementation complete for a user story.

**What to hand off:**
- Original spec.md (acceptance criteria)
- Implementation code
- Test results

**Expected output from verification:**
- Compliance report against spec
- Gap analysis
- Quality assessment

### To: backend-implementation-patterns

**Trigger:** `/speckit.plan` generated API contracts.

**What to hand off:**
- contracts/ directory (OpenAPI/GraphQL schemas)
- data-model.md (entity definitions)
- Technical context from plan.md

**Expected output:**
- Production API implementation
- Database migrations
- Middleware and error handling

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│                    SpecKit SDD Workflow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PRODUCT-REQUIREMENTS-DESIGNER (optional upstream)              │
│           │                                                     │
│           ▼                                                     │
│  /speckit.specify ──► spec.md + checklists/                     │
│           │                                                     │
│           ▼                                                     │
│  /speckit.plan ──► plan.md + research.md + data-model.md        │
│           │         + contracts/ + quickstart.md                 │
│           │                                                     │
│           ▼                                                     │
│  /speckit.tasks ──► tasks.md                                    │
│           │                                                     │
│           ├──────────────┬──────────────┬──────────────┐        │
│           ▼              ▼              ▼              ▼        │
│     TDD-WORKFLOW   BACKEND-IMPL   VERIFICATION   TESTING       │
│     (test-first)   (API build)    (compliance)   (strategy)    │
│           │              │              │              │        │
│           └──────────────┴──────────────┴──────────────┘        │
│                          │                                      │
│                          ▼                                      │
│             Working, verified implementation                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before handing off from speckit, verify:

- [ ] spec.md has no unresolved `[NEEDS CLARIFICATION]` markers
- [ ] All user stories have priority labels (P1, P2, P3)
- [ ] plan.md passes constitution gates (if constitution exists)
- [ ] contracts/ contains valid API specifications
- [ ] data-model.md defines all entities from spec
- [ ] tasks.md has numbered tasks (T001+) with story labels
- [ ] tasks.md has phase structure with dependencies documented

## Common Scenarios

### Greenfield Project

1. **product-requirements-designer:** Define product vision and features
2. **speckit:** `/speckit.specify` → `/speckit.plan` → `/speckit.tasks`
3. **github-repository-standards:** Structure repo per plan.md layout
4. **tdd-workflow:** Implement tasks with test-first approach
5. **verification-loop:** Validate each story against spec

### Existing Project — New Feature

1. **speckit:** `/speckit.specify` with existing project context
2. **speckit:** `/speckit.plan <existing-tech-stack>` — tech auto-detected
3. **speckit:** `/speckit.tasks` — tasks reference existing code paths
4. **backend-implementation-patterns:** Extend existing API
5. **testing-patterns:** Add tests following existing conventions

### Exploratory / Spike

1. **speckit:** `/speckit.specify` — lightweight spec with open questions
2. **speckit:** `/speckit.plan` — research phase resolves unknowns
3. Evaluate: Is the approach viable? Adjust spec if needed.
4. **speckit:** `/speckit.tasks` — only after research validates direction

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Skipping specify | Plans lack requirements traceability | Always start with `/speckit.specify` |
| Over-specifying | Analysis paralysis, spec never "done" | Max 3 `[NEEDS CLARIFICATION]` markers, then move on |
| Ignoring constitution | Plans violate project principles | Run constitution check in `/speckit.plan` |
| Monolithic tasks | Tasks too large to complete atomically | Each task should be one file or one function |
| Missing story labels | Can't trace tasks to requirements | Every task needs a `[USn]` label |
