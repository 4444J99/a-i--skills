---
name: continuous-learning-agent
description: Self-improvement patterns for AI agents to learn from feedback, errors, and successful patterns across sessions
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  adapted-by: ai-skills
  category: agent-improvement
governance_phases: [prove]
organ_affinity: [organ-iv]
triggers: [user-asks-about-agent-learning, context:ai-agents]
---

# Continuous Learning Agent

A meta-skill that enables AI agents to learn from experience and improve over time by separating journaled memory from policy changes that alter future behavior.

## Core Concept

Traditional agents reset completely between sessions. This skill treats memory and learning as related but distinct operations:
- **Journal / memory** records what happened, what was tried, and what evidence exists.
- **Learning / policy** changes what the agent will do next time for a recognizable event class.

Do not call a session log, decision journal, or context note "learning" unless it produces a policy delta, threshold revision, banned move, or acquired pattern that changes future behavior.

## Learning Mechanisms

Every learning loop has two layers:

1. **Journal layer**: episodic or semantic records used for auditability.
2. **Policy layer**: compact behavioral deltas used to improve performance on future tasks.

The journal layer is optional when an existing memory system already covers it. The policy layer is mandatory for this skill.

### 1. Error Pattern Recognition

After each error, first document the event if no existing memory system already captures it:

```markdown
## Error Log Entry

**Date**: 2026-01-30
**Context**: Implementing user authentication
**Error**: TypeError: Cannot read property 'id' of undefined
**Root Cause**: Missing null check before accessing user object
**Fix**: Added optional chaining: user?.id
**Pattern**: Always validate object existence before property access
**Prevention**: Add TypeScript strict null checks
```

Then extract the policy delta:

```markdown
## Policy Delta: [Short Title]

**Date**: 2026-01-30
**Event Class**: Accessing nested properties on possibly absent objects
**Prior Policy**: Read nested properties directly after optimistic object construction.
**Failure Mode**: Undefined objects caused runtime TypeErrors.
**Revised Policy**: Validate object existence or use typed optional access before nested reads.
**Trigger**: Any code path receiving user, API, database, or tool-returned objects.
**Propagation Target**: Project AGENTS.md, test helper, lint rule, or skill source.
**Verification**: Add or run a test that fails under the prior policy and passes under the revised policy.
```

### 2. Success Pattern Collection

After successful implementations, record both the reusable pattern and the policy form that lets future agents apply it without replaying the whole story:

```markdown
## Success Pattern

**Task**: Add pagination to API endpoint
**Approach**: Cursor-based pagination with encoded tokens
**Why It Worked**: Handles large datasets efficiently, stateless
**Reusable Pattern**: 
- Use cursor tokens instead of offset/limit
- Encode cursor with base64
- Include hasNext/hasPrevious flags
- Return next/previous cursor in response

**Code Template**:
\`\`\`typescript
interface PaginatedResponse<T> {
  data: T[];
  cursor: {
    next: string | null;
    previous: string | null;
  };
}
\`\`\`
```

```markdown
## Acquired Pattern

**Event Class**: API endpoints returning large ordered datasets
**Revised Policy**: Prefer cursor tokens over offset pagination unless the product explicitly needs random page access.
**Trigger**: New list endpoint over a growing table or external API collection.
**Verification**: Exercise first page, next page, empty page, and invalid cursor behavior.
```

### 3. Feedback Integration

Use the active project's policy surface when one exists. Examples:
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or other runtime instruction files for enduring operating rules.
- `.claude/policy/`, `.codex/policy/`, `.agents/policy/`, or equivalent for local policy deltas.
- A governed memory or feedback-note repository when the user has established one.

Only create a local journal directory when there is no stronger existing memory surface:

```bash
mkdir -p .claude/journal .claude/policy/deltas
```

Store journal records and policy deltas separately:

```
.claude/journal/
  patterns/
    authentication.md
    database-queries.md
    error-handling.md
  mistakes/
    common-bugs.md
    performance-issues.md
  preferences/
    code-style.md
    testing-approach.md
    naming-conventions.md
.claude/policy/
  deltas/
    2026-01-30-null-check-before-property-access.md
  banned-moves.md
  thresholds.md
  acquired-patterns.md
```

### 4. Decision Journal

Before major decisions:

```markdown
## Decision: [Title]

**Context**: Current situation requiring decision
**Options Considered**:
1. Option A - Pros: X, Cons: Y
2. Option B - Pros: X, Cons: Y
3. Option C - Pros: X, Cons: Y

**Decision**: Chose Option B
**Reasoning**: Detailed explanation
**Expected Outcome**: What we expect to happen
**Actual Outcome**: (Fill after implementation)
**Policy Delta**: What future behavior changes because of this decision
```

## Learning Loops

### Daily Review Loop

At end of coding session:

```markdown
## Session Review - [Date]

**What Went Well**:
- Successfully implemented X
- Discovered pattern Y
- Improved performance of Z

**What Could Improve**:
- Spent too long debugging A
- Should have tested B earlier
- Missed edge case C

**Journal Notes**:
1. Notable event 1
2. Notable event 2

**Policy Deltas**:
1. Event class -> revised behavior
2. Event class -> revised threshold

**Action Items**:
- [ ] Apply policy delta to the correct instruction or policy file
- [ ] Verify the new behavior with a test, checklist, or next-session review
```

### Weekly Synthesis Loop

Every week, review and synthesize:

```bash
# Generate weekly summary
grep -h "^**Policy Deltas**" .claude/journal/daily/*.md -A 5 > weekly-policy-synthesis.md
```

```markdown
## Weekly Synthesis - Week of [Date]

**Emerging Policy Changes**:
- Pattern 1: Description
- Pattern 2: Description

**Recurring Issues**:
- Issue 1: Root cause analysis
- Issue 2: Root cause analysis

**Rules to Promote**:
- Rule 1: Target file and reason
- Rule 2: Target file and reason

**Next Week Focus**:
- Focus area 1
- Focus area 2
```

## Adaptive Strategies

### Context Awareness

Maintain context file:

```markdown
# Project Context

**Type**: Web application / API / CLI tool / Library
**Tech Stack**: Next.js, TypeScript, Prisma, PostgreSQL
**Architecture**: Monorepo with packages: api, web, shared
**Key Patterns**: 
- Feature-based folder structure
- Repository pattern for data access
- Service layer for business logic

**Team Preferences**:
- Test coverage: 80% minimum
- Code style: Prettier + ESLint
- Commit messages: Conventional commits
- PR process: Requires review + CI pass
```

### Progressive Refinement

Track understanding level:

```markdown
## Understanding Map

**Well Understood** (★★★):
- Authentication flow
- Database schema
- API endpoints

**Partially Understood** (★★):
- Caching strategy
- Error handling patterns

**Need to Learn** (★):
- Deployment process
- Monitoring setup
- Feature flags system
```

## Implementation Hooks

### Post-Task Hook

After completing any task:

```bash
#!/bin/bash
# .claude/hooks/post-task.sh

echo "## Task Completed: $1" >> .claude/journal/daily/$(date +%Y-%m-%d).md
echo "" >> .claude/journal/daily/$(date +%Y-%m-%d).md
echo "**Approach**: $2" >> .claude/journal/daily/$(date +%Y-%m-%d).md
echo "**Outcome**: $3" >> .claude/journal/daily/$(date +%Y-%m-%d).md
echo "**Policy Delta**: $4" >> .claude/journal/daily/$(date +%Y-%m-%d).md
echo "" >> .claude/journal/daily/$(date +%Y-%m-%d).md
```

### Pre-Task Hook

Before starting task:

```bash
#!/bin/bash
# .claude/hooks/pre-task.sh

# Check for similar past tasks
echo "Checking learnings for: $1"
grep -r "$1" .claude/policy .claude/journal 2>/dev/null | head -5

# Check for known pitfalls
grep -r "mistake.*$1" .claude/policy .claude/journal 2>/dev/null
```

## Knowledge Base Structure

```
.claude/
  journal/
    daily/
      2026-01-30.md
      2026-01-29.md
    weekly/
      2026-week-05.md
    patterns/
      successful/
        authentication-patterns.md
        api-design-patterns.md
      antipatterns/
        common-mistakes.md
        performance-pitfalls.md
    context/
      project-overview.md
      tech-stack.md
      team-preferences.md
    decisions/
      architecture-decisions.md
      technology-choices.md
  policy/
    deltas/
      2026-01-30-null-check-before-property-access.md
    acquired-patterns.md
    banned-moves.md
    thresholds.md
```

## Querying Past Learnings

### Find Similar Solutions

```bash
# Search for pattern
grep -r "pagination" .claude/policy .claude/journal/patterns/

# Find past mistakes
grep -r "TypeError" .claude/policy .claude/journal/mistakes/

# Check decisions
grep -r "decision.*database" .claude/journal/decisions/
```

### Extract Patterns

```bash
# Get all successful patterns
grep -h "^## Success Pattern" .claude/journal/patterns/successful/*.md

# Get all lessons learned
grep -h "^**Policy Delta**" .claude/journal .claude/policy -R -A 3
```

## Integration Points

Complements:
- **knowledge-architecture**: For organizing learnings
- **second-brain-librarian**: For long-term knowledge storage
- **verification-loop**: For quality feedback
- **project-orchestration**: For applying learnings to planning

## Progressive Enhancement

As agent improves:

**Level 1**: Basic journal logging
**Level 2**: Policy delta extraction
**Level 3**: Policy propagation into the right instruction surface
**Level 4**: Verification that future behavior changed
**Level 5**: Autonomous decision-making within approved constraints

Track current level and progression metrics.

## Metrics

Track improvement:

```markdown
## Agent Performance Metrics

**Error Rate**: Errors per task over time
**Pattern Reuse**: How often policy deltas are applied
**Decision Quality**: Outcome vs. expected outcome alignment
**Context Accuracy**: How well agent understands project
**Adaptation Speed**: Time to learn new patterns
**Propagation Rate**: How often journaled lessons become active policy

**Trend**: Improving / Stable / Declining
```

## Initialization

First time setup:

```bash
# Create journal and policy infrastructure
mkdir -p .claude/journal/{daily,weekly,patterns,mistakes,context,decisions}
mkdir -p .claude/policy/deltas

# Initialize context file
cat > .claude/journal/context/project-overview.md << 'EOF'
# Project Overview
- Project type:
- Tech stack:
- Architecture:
- Key files:
EOF

# Create first session log
date +%Y-%m-%d > .claude/journal/daily/$(date +%Y-%m-%d).md
```

Start every session by reviewing active policy first, then journal records only when they are relevant to the task.
