---
name: stranger-test-protocol
description: Validate that documentation, READMEs, and onboarding guides are comprehensible to someone with zero prior context. Systematic approach to testing docs from a stranger's perspective with actionable feedback. Triggers on documentation review, onboarding validation, or README quality assessment requests.
license: MIT
complexity: beginner
time_to_learn: 30min
tags:
  - documentation
  - onboarding
  - review
  - readability
  - stranger-test
governance_phases: [prove]
governance_norm_group: documentation-standard
governance_auto_activate: true
organ_affinity: [all]
triggers: [user-asks-about-doc-review, context:documentation-quality, context:onboarding-review, context:readme-review, context:stranger-test]
complements: [github-repository-standards, technical-analytical-writing, repo-onboarding-flow]
---

# Stranger Test Protocol

Evaluate documentation from the perspective of someone encountering the project for the first time.

## The Stranger Test

The Stranger Test asks: **"Could a competent developer with zero context about this project understand what it does, why it exists, and how to get started — in under 5 minutes?"**

## Evaluation Framework

### Level 1: First Contact (30 seconds)

Evaluate the README's first screen:

| Criterion | Pass | Fail |
|-----------|------|------|
| **What is it?** | Clear one-sentence description | Jargon, acronyms, or missing |
| **Who is it for?** | Target audience stated or obvious | Unclear audience |
| **Why does it exist?** | Problem/value stated | No motivation |
| **Is it alive?** | Recent activity, badges, dates | No signals of maintenance |

### Level 2: Comprehension (2 minutes)

Evaluate understanding after reading the full README:

| Criterion | Pass | Fail |
|-----------|------|------|
| **Architecture** | Can sketch the system on a napkin | Opaque internal terminology |
| **Key concepts** | Core abstractions defined | Assumes prior knowledge |
| **Scope boundaries** | Clear what it does and doesn't do | Ambiguous scope |
| **Relationship to ecosystem** | How it fits with other tools | Exists in a vacuum |

### Level 3: Activation (5 minutes)

Evaluate the getting-started experience:

| Criterion | Pass | Fail |
|-----------|------|------|
| **Prerequisites** | Listed explicitly | Discovered through errors |
| **Install steps** | Copy-pasteable commands | Incomplete or stale |
| **First success** | Can run hello-world | Errors before first output |
| **Next steps** | Clear path forward | Dead end after install |

## Conducting the Test

### Step 1: Adopt the Stranger Mindset

Temporarily forget all context about the project. Read as if encountering it on GitHub for the first time. Note every moment of confusion, even if you "know the answer."

### Step 2: Sequential Read-Through

Read the documentation in this order, timing each section:

1. Repository name and description
2. README.md (top to bottom)
3. First linked guide (if any)
4. First code example (if any)

### Step 3: Record Confusion Points

For each confusion point, record:

```markdown
- **Location:** README.md, line 23
- **Confusion:** "What is an 'organ' in this context? The term is used 5 times before being defined."
- **Severity:** High (blocks understanding of everything that follows)
- **Fix:** Add a one-sentence definition before first use, or link to glossary.
```

### Step 4: Assess Each Level

Score each criterion as PASS, PARTIAL, or FAIL. Provide evidence.

### Step 5: Produce Report

```markdown
## Stranger Test Report: {project-name}

**Tester:** {name/role}
**Date:** {date}
**Time to first understanding:** {seconds}
**Time to first success:** {minutes, or "did not achieve"}

### Level 1: First Contact — {PASS/PARTIAL/FAIL}
{findings}

### Level 2: Comprehension — {PASS/PARTIAL/FAIL}
{findings}

### Level 3: Activation — {PASS/PARTIAL/FAIL}
{findings}

### Confusion Points (ordered by severity)
1. {point}
2. {point}

### Recommendations (ordered by impact)
1. {recommendation}
2. {recommendation}
```

## Common Failures

### Jargon Without Definition

**Bad:** "This repo manages the Taxis orchestration layer for the ORGANVM eight-organ model."

**Good:** "This repo orchestrates automated workflows across ORGANVM — a system that organizes ~100 repositories into 8 functional groups ('organs') covering theory, art, commerce, and governance."

### Missing Prerequisites

**Bad:**
```bash
npm install
npm start
```

**Good:**
```bash
# Prerequisites: Node.js 20+, npm 10+
# Verify: node --version && npm --version
npm install
npm start
# Open http://localhost:3000 — you should see the dashboard
```

### Assumed Context

**Bad:** "See the governance rules for promotion constraints."

**Good:** "See the promotion-readiness-checklist skill for promotion constraints defining the state machine."

### Dead-End Documentation

**Bad:** README ends after install instructions.

**Good:** README includes "What's Next" section with 3-4 concrete next steps.

## Applying to Different Document Types

### README

Focus on Level 1 and Level 3. The README is the front door — it must answer "what" and "how to start" immediately.

### API Documentation

Focus on Level 2 and Level 3. Developers need to understand concepts and make their first API call quickly.

### Contributing Guide

Focus on Level 3 heavily. The reader is motivated but needs a clear path from "I want to help" to "I submitted a PR."

### Architecture Docs

Focus on Level 2. Can a new team member understand the system well enough to know where to make changes?

## Integration with CI

```yaml
# Reminder in PR template
- [ ] Stranger test: Could a new contributor understand this PR's context from the linked docs?
- [ ] New concepts introduced in this PR are defined before first use
- [ ] Commands in documentation are copy-pasteable and tested
```

## Anti-Patterns

- **Testing your own docs** — The author cannot be the stranger; fresh eyes are essential
- **"It's obvious"** — If it needs to be said, it's not obvious to a stranger
- **Fixing symptoms** — "Add a glossary" treats the symptom; "define terms on first use" treats the cause
- **One-time test** — Run the stranger test after every major documentation change
- **Perfectionism** — A PARTIAL pass with an action plan beats never testing at all
