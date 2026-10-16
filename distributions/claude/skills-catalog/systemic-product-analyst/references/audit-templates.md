# Product Audit Templates

Ready-to-use templates for systematic product analysis.

## Snapshot Template

```markdown
# $THING_SNAPSHOT

## Meta
- **Date:** YYYY-MM-DD
- **Auditor:**
- **Version/State:**

## North Star Metric
- **Metric:** [Single number that matters]
- **Current Value:**
- **Target Value:**
- **Trend:** ↑ ↓ →

## Primary User
- **Who:** [Specific description]
- **Context:** [When/where they use it]
- **Job to be Done:** [What they're trying to accomplish]

## Current State Summary

### What Exists
- [ ] Working product/prototype
- [ ] Public presence (website, repo)
- [ ] Active users
- [ ] Revenue

### Recent Changes
1. [Change 1]
2. [Change 2]
3. [Change 3]

### Known Issues
1. [Issue 1]
2. [Issue 2]
```

---

## Scorecard Template

```markdown
# $SCORECARD

## Lane A: The Thing Itself (Build Truth)

| Criterion | Score (1-5) | Evidence | Notes |
|-----------|-------------|----------|-------|
| **Outcome Reliability** | | | Does it work consistently? |
| **Time-to-Value** | | | How fast does user get value? |
| **Architecture Clarity** | | | Is it maintainable? |
| **Defensibility** | | | Moats, data advantages? |

**Lane A Total:** _/20

## Lane B: The Thing in the World (World Interface)

| Criterion | Score (1-5) | Evidence | Notes |
|-----------|-------------|----------|-------|
| **Positioning** | | | Clear who it's for/not for? |
| **Trust (Claim vs Proof)** | | | Can claims be verified? |
| **Discovery** | | | How do users find it? |
| **Monetization** | | | Clear value-to-cash path? |

**Lane B Total:** _/20

## Mismatch Analysis

Lane A Score: _
Lane B Score: _
Gap: _

**Diagnosis:**
- [ ] Best Kept Secret (A > B) → Focus on distribution
- [ ] Vaporware (B > A) → Focus on product
- [ ] Balanced → Continue execution

## Priority Recommendation
[One sentence: What to focus on next]
```

---

## Risk Register Template

```markdown
# $RISK_REGISTER

## Critical Risks (Could kill the project)

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| | H/M/L | H/M/L | | |
| | | | | |

## High Risks (Major setback)

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| | H/M/L | H/M/L | | |
| | | | | |

## Medium Risks (Manageable friction)

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| | H/M/L | H/M/L | | |
| | | | | |

## Risk Categories

### Build Risks (Lane A)
- Technical debt
- Scalability
- Single point of failure
- Key person dependency

### Market Risks (Lane B)
- Competition
- Timing
- Distribution dependency
- Pricing pressure

### Execution Risks
- Resource constraints
- Team dynamics
- External dependencies
- Regulatory
```

---

## 30/60/90 Day Plan Template

```markdown
# $NEXT_30_60_90

## Guiding Principles
- **North Star:** [Metric]
- **Key Constraint:** [The one thing that limits everything]
- **Mismatch Focus:** [Build / Distribution]

---

## Days 1-30: Foundation

### Lane A (Build) - ONE deep change
**Goal:**
**Success Metric:**
**Tasks:**
- [ ]
- [ ]
- [ ]

### Lane B (World) - ONE interface change
**Goal:**
**Success Metric:**
**Tasks:**
- [ ]
- [ ]
- [ ]

### Blockers to Remove
1.
2.

---

## Days 31-60: Validation

### Lane A (Build)
**Goal:**
**Success Metric:**
**Tasks:**
- [ ]
- [ ]

### Lane B (World)
**Goal:**
**Success Metric:**
**Tasks:**
- [ ]
- [ ]

### Checkpoint Questions
- Is the North Star moving?
- What surprised us?
- What do we stop doing?

---

## Days 61-90: Scale

### Lane A (Build)
**Goal:**
**Success Metric:**
**Tasks:**
- [ ]
- [ ]

### Lane B (World)
**Goal:**
**Success Metric:**
**Tasks:**
- [ ]
- [ ]

### 90-Day Review Questions
- Did we hit North Star target?
- What's the new constraint?
- What's the next 30/60/90?
```

---

## Friction Map Template

```markdown
# Friction Map

## Accidental Friction (Bad design)

| Location | Description | Severity | Fix Effort |
|----------|-------------|----------|------------|
| | | H/M/L | H/M/L |
| | | | |

## Deceptive Friction (Broken promises)

| Claim | Reality | Trust Impact | Fix |
|-------|---------|--------------|-----|
| | | | |
| | | | |

## Intentional Friction (By design)

| Location | Purpose | Still Valid? |
|----------|---------|--------------|
| | | Y/N |
| | | |

## Priority Order
1. Fix deceptive friction first (trust)
2. Remove accidental friction (experience)
3. Review intentional friction (strategy)
```

---

## Claim Stack Template

```markdown
# Claim Stack Analysis

## Top 3 Claims

### Claim 1: "[Exact claim made]"
- **Location:** [Where this claim appears]
- **Proof Type:** Demo / Data / Testimonial / None
- **Proof Strength:** Strong / Weak / Missing
- **Verdict:** ✓ Verified / ⚠️ Partial / ✗ Unverified

### Claim 2: "[Exact claim made]"
- **Location:**
- **Proof Type:**
- **Proof Strength:**
- **Verdict:**

### Claim 3: "[Exact claim made]"
- **Location:**
- **Proof Type:**
- **Proof Strength:**
- **Verdict:**

## Summary
- Claims verified: _/3
- Trust gap: [Description]
- Action: [What to do about unverified claims]
```
