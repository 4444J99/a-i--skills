---
name: continuous-learning-agent
description: Self-improvement patterns for AI agents to learn from feedback, errors, and successful patterns across sessions
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  adapted-by: ai-skills
  category: agent-improvement
---

# Continuous Learning Agent

A meta-skill that enables AI agents to learn from experience and improve over time through systematic feedback collection and pattern recognition.

## Core Concept

Traditional agents reset completely between sessions. This skill implements memory and learning mechanisms to:
- Learn from mistakes
- Recognize successful patterns
- Build context over time
- Adapt to user preferences
- Improve decision-making

## Learning Mechanisms

### 1. Error Pattern Recognition

After each error, document:

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

### 2. Success Pattern Collection

After successful implementations:

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

### 3. Feedback Integration

Create `.claude/learnings/` directory:

```bash
mkdir -p .claude/learnings
```

Store learnings in categorized files:

```
.claude/learnings/
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
**Lessons Learned**: What we learned from this decision
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

**Key Learnings**:
1. Learning point 1
2. Learning point 2
3. Learning point 3

**Action Items**:
- [ ] Document pattern X
- [ ] Create helper for Y
- [ ] Add test for Z
```

### Weekly Synthesis Loop

Every week, review and synthesize:

```bash
# Generate weekly summary
cat .claude/learnings/daily/*.md | grep "Key Learnings" -A 3 > weekly-synthesis.md
```

```markdown
## Weekly Synthesis - Week of [Date]

**Emerging Patterns**:
- Pattern 1: Description
- Pattern 2: Description

**Recurring Issues**:
- Issue 1: Root cause analysis
- Issue 2: Root cause analysis

**Skills Improved**:
- Skill 1: How it improved
- Skill 2: How it improved

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

echo "## Task Completed: $1" >> .claude/learnings/daily/$(date +%Y-%m-%d).md
echo "" >> .claude/learnings/daily/$(date +%Y-%m-%d).md
echo "**Approach**: $2" >> .claude/learnings/daily/$(date +%Y-%m-%d).md
echo "**Outcome**: $3" >> .claude/learnings/daily/$(date +%Y-%m-%d).md
echo "**Learning**: $4" >> .claude/learnings/daily/$(date +%Y-%m-%d).md
echo "" >> .claude/learnings/daily/$(date +%Y-%m-%d).md
```

### Pre-Task Hook

Before starting task:

```bash
#!/bin/bash
# .claude/hooks/pre-task.sh

# Check for similar past tasks
echo "Checking learnings for: $1"
grep -r "$1" .claude/learnings/ | head -5

# Check for known pitfalls
grep -r "mistake.*$1" .claude/learnings/mistakes/
```

## Knowledge Base Structure

```
.claude/
  learnings/
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
```

## Querying Past Learnings

### Find Similar Solutions

```bash
# Search for pattern
grep -r "pagination" .claude/learnings/patterns/

# Find past mistakes
grep -r "TypeError" .claude/learnings/mistakes/

# Check decisions
grep -r "decision.*database" .claude/learnings/decisions/
```

### Extract Patterns

```bash
# Get all successful patterns
grep -h "^## Success Pattern" .claude/learnings/patterns/successful/*.md

# Get all lessons learned
grep -h "^**Lessons Learned**" .claude/learnings/ -A 3
```

## Integration Points

Complements:
- **knowledge-architecture**: For organizing learnings
- **second-brain-librarian**: For long-term knowledge storage
- **verification-loop**: For quality feedback
- **project-orchestration**: For applying learnings to planning

## Progressive Enhancement

As agent improves:

**Level 1**: Basic error logging
**Level 2**: Pattern recognition
**Level 3**: Automated suggestions
**Level 4**: Proactive guidance
**Level 5**: Autonomous decision-making within constraints

Track current level and progression metrics.

## Metrics

Track improvement:

```markdown
## Agent Performance Metrics

**Error Rate**: Errors per task over time
**Pattern Reuse**: How often learned patterns are applied
**Decision Quality**: Outcome vs. expected outcome alignment
**Context Accuracy**: How well agent understands project
**Adaptation Speed**: Time to learn new patterns

**Trend**: Improving / Stable / Declining
```

## Initialization

First time setup:

```bash
# Create learning infrastructure
mkdir -p .claude/learnings/{daily,weekly,patterns,mistakes,context,decisions}

# Initialize context file
cat > .claude/learnings/context/project-overview.md << 'EOF'
# Project Overview
- Project type:
- Tech stack:
- Architecture:
- Key files:
EOF

# Create first session log
date +%Y-%m-%d > .claude/learnings/daily/$(date +%Y-%m-%d).md
```

Start every session by reviewing recent learnings.
