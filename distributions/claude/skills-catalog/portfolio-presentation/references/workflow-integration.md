# Workflow Integration: Portfolio Presentation

This document describes how `portfolio-presentation` integrates with other skills in the Career Development ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `brand-guidelines` | **Upstream** | Receive identity for portfolio |
| `cv-resume-builder` | **Downstream** | Provide examples for resume |
| `interview-preparation` | **Downstream** | Provide discussion examples |
| `networking-outreach` | **Complementary** | Share work in networking |

## Prerequisites

Before invoking `portfolio-presentation`, ensure:

1. **Work inventory available** - Projects and achievements to consider
2. **Target audience known** - Who will view the portfolio
3. **Presentation medium decided** - Website, PDF, slides

## Handoff Patterns

### From: brand-guidelines

**Trigger:** Brand identity ready to apply.

**What to receive:**
- Visual identity elements
- Voice and tone
- Positioning statement
- Key themes

**Integration points:**
- Consistent visual design
- Project narrative voice
- Thematic organization

### To: cv-resume-builder

**Trigger:** Portfolio curated for resume.

**What to hand off:**
- Project summaries
- Quantified impact
- Key achievements
- Skills demonstrated

**Expected output from resume:**
- Resume bullets from portfolio
- Linked portfolio URL
- Achievement highlights

### To: interview-preparation

**Trigger:** Portfolio ready for discussion.

**What to hand off:**
- Project details and context
- Challenge/solution narratives
- Metrics and outcomes
- Lessons learned

**Expected output from interview prep:**
- STAR stories from projects
- Technical deep dives
- Presentation practice

### To: networking-outreach

**Trigger:** Portfolio ready to share.

**What to hand off:**
- Portfolio URL or assets
- Project highlights
- Talking points
- Context for each connection

**Expected output from networking:**
- Sharing opportunities
- Feedback collection
- Introduction contexts

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Portfolio Development                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. BRAND-GUIDELINES: Define visual and verbal identity    │
│           │                                                 │
│           ▼                                                 │
│  2. PORTFOLIO-PRESENTATION: Curate and present work        │
│           │                                                 │
│           ├─────────────────────┬─────────────────┐         │
│           ▼                     ▼                 ▼         │
│      CV-RESUME             INTERVIEW          NETWORKING   │
│      BUILDER               PREPARATION        OUTREACH     │
│      (resume content)      (story examples)   (sharing)    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing portfolio, verify:

- [ ] Best work prominently featured
- [ ] Context and challenge clear for each project
- [ ] Results and impact quantified
- [ ] Visual presentation polished
- [ ] Easy to navigate
- [ ] Mobile-friendly (if web)
- [ ] Contact information visible
- [ ] Updated with recent work

## Common Scenarios

### Career Transition Portfolio

1. **Brand Guidelines:** New positioning
2. **Portfolio Presentation:** Reframe existing work
3. **CV Resume Builder:** Transition-focused resume

### Design Portfolio

1. **Brand Guidelines:** Visual identity
2. **Portfolio Presentation:** Case study format
3. **Networking Outreach:** Design community sharing

### Technical Portfolio

1. **Portfolio Presentation:** Code samples and projects
2. **Interview Preparation:** Technical discussion prep
3. **CV Resume Builder:** Technical skills section

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Everything included | Dilutes best work | Curate ruthlessly |
| No context | Work doesn't make sense | Add case study narratives |
| Outdated work | Shows stale skills | Regular updates |
| Poor presentation | Undermines quality | Invest in design |

## Related Resources

- [Career Development Skills Ecosystem Map](../../../docs/guides/career-development-skills-ecosystem.md)
