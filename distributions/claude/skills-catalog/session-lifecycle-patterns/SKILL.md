---
name: session-lifecycle-patterns
description: Manage AI agent session lifecycles with structured phases (FRAME, SHAPE, BUILD, PROVE), context preservation across sessions, handoff protocols, and session metadata tracking. Triggers on session management, agent lifecycle, or multi-session workflow requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - session-management
  - agent-lifecycle
  - context-preservation
  - workflow-phases
governance_phases: [shape, build, prove]
organ_affinity: [all]
triggers: [user-asks-about-session-management, context:agent-sessions, context:workflow-phases, context:session-handoff]
complements: [cross-agent-handoff, prompt-engineering-patterns, agent-swarm-orchestrator]
---

# Session Lifecycle Patterns

Structure AI agent sessions for predictable outcomes, context preservation, and clean handoffs.

## The Phase Model

```
FRAME → SHAPE → BUILD → PROVE → DONE
  ↑       ↑       ↑       ↑
  └───────┴───────┴───────┘
     (back-transitions allowed)
```

### Phase Definitions

| Phase | Purpose | Activities | Gate |
|-------|---------|-----------|------|
| **FRAME** | Understand context | Explore code, read docs, ask questions | Can articulate the problem |
| **SHAPE** | Design approach | Create plan, identify files, consider tradeoffs | Plan reviewed and approved |
| **BUILD** | Implement | Write code, create files, apply changes | Implementation complete |
| **PROVE** | Verify | Run tests, validate output, check quality | All checks pass |
| **DONE** | Close | Summarize, commit, document decisions | Session artifacts preserved |

### Phase Transitions

```python
VALID_TRANSITIONS = {
    "FRAME": ["SHAPE"],
    "SHAPE": ["FRAME", "BUILD"],       # Can go back to reframe
    "BUILD": ["SHAPE", "PROVE"],       # Can go back to reshape
    "PROVE": ["BUILD", "DONE"],        # Can go back to fix
    "DONE": [],                        # Terminal
}

def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])
```

### Phase Anti-Patterns

- **Skipping FRAME** — Jumping to code without understanding the problem
- **SHAPE → BUILD without approval** — Building before alignment on approach
- **Staying in BUILD forever** — Not proving that the work is correct
- **PROVE → DONE without evidence** — Claiming completion without verification

## Session Metadata

### Session Record Structure

```yaml
session:
  id: "sess_2026-03-20_a1b2c3"
  started: "2026-03-20T10:58:00Z"
  ended: "2026-03-20T12:30:00Z"
  phase_history:
    - phase: FRAME
      entered: "2026-03-20T10:58:00Z"
      duration_minutes: 15
    - phase: SHAPE
      entered: "2026-03-20T11:13:00Z"
      duration_minutes: 20
    - phase: BUILD
      entered: "2026-03-20T11:33:00Z"
      duration_minutes: 45
    - phase: PROVE
      entered: "2026-03-20T12:18:00Z"
      duration_minutes: 12
  scope:
    organ: IV
    repo: a-i--skills
    task: "Create python-packaging-patterns skill"
  artifacts:
    files_created: [skills/development/python-packaging-patterns/SKILL.md]
    files_modified: []
    commits: ["abc123"]
  decisions:
    - "Chose hatchling as recommended build backend"
    - "Included namespace package pattern for multi-repo use"
```

## Context Preservation

### Intra-Session Context

Maintain context as the session progresses through phases:

```python
class SessionContext:
    def __init__(self):
        self.discoveries: list[str] = []   # FRAME findings
        self.plan: dict = {}               # SHAPE output
        self.changes: list[str] = []       # BUILD artifacts
        self.evidence: list[str] = []      # PROVE results

    def frame_discovery(self, finding: str):
        self.discoveries.append(finding)

    def shape_decision(self, key: str, value: str, rationale: str):
        self.plan[key] = {"value": value, "rationale": rationale}
```

### Inter-Session Context

For multi-session work, preserve essential context at session end:

```markdown
## Session Close Summary

### What was accomplished
- Created 6 Wave 0 skills (python-packaging-patterns through vector-search-patterns)

### What remains
- 18 more Wave 0 skills in Batches 2-4
- Waves 1-4 pending

### Key decisions
- Using governance_norm_group: repo-hygiene for packaging/config skills
- Using organ_affinity: [all] for cross-cutting infrastructure skills

### Blockers
- None

### Next session should start by
- Reading this summary
- Continuing with Wave 0 Batch 2
```

## Session Types

### Exploration Session

```
FRAME (80%) → SHAPE (20%) → DONE
```

Heavy on reading, light on planning, no implementation. Produces understanding and a plan for a future BUILD session.

### Implementation Session

```
FRAME (10%) → SHAPE (15%) → BUILD (55%) → PROVE (20%) → DONE
```

Quick reorientation, then focused building and verification.

### Debug Session

```
FRAME (40%) → BUILD (30%) → PROVE (30%) → DONE
```

Heavy investigation, targeted fix, thorough verification.

### Review Session

```
FRAME (30%) → PROVE (70%) → DONE
```

Mostly reading and validating existing work.

## Multi-Session Continuity

### Session Chains

When work spans multiple sessions, each session references the chain:

```yaml
chain:
  id: "skill-fortification-campaign"
  session_index: 3
  total_sessions_estimated: 15
  previous_session: "sess_2026-03-20_wave0-batch1"
  completed_items: ["A1", "A2", "A3", "A4", "A5", "A6"]
  remaining_items: ["A7", "A8", "A13", "A14", "B1", "B2", ...]
```

### Handoff Protocol

At session end, produce a handoff document:

1. **State snapshot** — What exists now (files, branches, test status)
2. **Decision log** — Why choices were made (so next session doesn't re-litigate)
3. **Next actions** — Exactly what to do next, with no ambiguity
4. **Risk flags** — Anything the next session should watch for

## Session Quality Signals

| Signal | Healthy | Unhealthy |
|--------|---------|-----------|
| Phase transitions | Sequential with occasional back-steps | Skipping phases, staying in one phase |
| FRAME duration | 10-30% of session | <5% or >50% |
| PROVE evidence | Concrete test/validation output | "I think this works" |
| Context preserved | Summary written at DONE | Session ends abruptly |
| Scope creep | Stays within stated scope | Expanding mid-BUILD |

## Anti-Patterns

- **Infinite FRAME** — Analysis paralysis; at some point, start shaping
- **Skipping PROVE** — Every BUILD must be proved before DONE
- **No session close** — Always write a summary, even if brief
- **Context loss between sessions** — Handoff documents are mandatory for multi-session work
- **Phase theater** — Going through motions without substance in each phase
