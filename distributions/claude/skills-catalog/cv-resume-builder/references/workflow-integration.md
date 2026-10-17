# Workflow Integration: CV Resume Builder

This document describes how `cv-resume-builder` integrates with other skills in the Career Development ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `brand-guidelines` | **Upstream** | Receive voice and positioning |
| `portfolio-presentation` | **Upstream** | Source achievement examples |
| `interview-preparation` | **Downstream** | Resume opens interviews |
| `networking-outreach` | **Complementary** | Resume for introductions |

## Prerequisites

Before invoking `cv-resume-builder`, ensure:

1. **Target role defined** - What job you're applying for
2. **Personal brand clear** - Your value proposition
3. **Work examples available** - Achievements to highlight

## Handoff Patterns

### From: brand-guidelines

**Trigger:** Brand identity ready to apply.

**What to receive:**
- Voice and tone guidelines
- Positioning statement
- Value proposition
- Key differentiators

**Integration points:**
- Summary section voice
- Consistent terminology
- Headline positioning

### From: portfolio-presentation

**Trigger:** Work curated for targeting.

**What to receive:**
- Achievement metrics
- Project summaries
- Impact statements
- Relevant skill demonstrations

**Integration points:**
- Experience bullet points
- Quantified achievements
- Skills section evidence

### To: interview-preparation

**Trigger:** Resume submitted, interview scheduled.

**What to hand off:**
- Resume copy for reference
- Key stories behind bullets
- Potential question areas
- Gaps that may need addressing

**Expected output from interview prep:**
- Story versions of resume points
- Gap bridging strategies
- Question anticipation

### To: networking-outreach

**Trigger:** Resume ready for sharing.

**What to hand off:**
- Resume PDF
- Key talking points
- Target role description
- Ask/request

**Expected output from networking:**
- Connection introductions
- Company referrals
- Feedback on positioning

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Resume Creation Flow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. BRAND-GUIDELINES: Define voice and positioning         │
│           │                                                 │
│           ▼                                                 │
│  2. PORTFOLIO-PRESENTATION: Curate relevant work           │
│           │                                                 │
│           ▼                                                 │
│  3. CV-RESUME-BUILDER: Create targeted resume              │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. NETWORKING-OUTREACH      4b. INTERVIEW-PREPARATION    │
│      (share resume)               (prepare stories)        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing resume, verify:

- [ ] Matches target role requirements
- [ ] ATS-compatible formatting
- [ ] Quantified achievements where possible
- [ ] Consistent voice with brand
- [ ] No typos or grammatical errors
- [ ] Contact information accurate
- [ ] Links work (LinkedIn, portfolio)
- [ ] One page (or appropriate length)

## Common Scenarios

### New Grad Resume

1. **Portfolio Presentation:** Curate projects and coursework
2. **Brand Guidelines:** Define early-career positioning
3. **CV Resume Builder:** Create entry-level resume

### Senior Professional Resume

1. **Brand Guidelines:** Executive positioning
2. **Portfolio Presentation:** Leadership achievements
3. **CV Resume Builder:** Strategic resume

### Career Change Resume

1. **Portfolio Presentation:** Identify transferable work
2. **Brand Guidelines:** Reposition narrative
3. **CV Resume Builder:** Functional/combination format

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Generic resume | Doesn't stand out | Target each application |
| Wall of text | Not scannable | Use bullets and white space |
| Responsibilities over achievements | Doesn't show impact | Lead with results |
| Outdated format | Looks dated | Use modern, clean design |

## Related Resources

- [Career Development Skills Ecosystem Map](../../../docs/guides/career-development-skills-ecosystem.md)
