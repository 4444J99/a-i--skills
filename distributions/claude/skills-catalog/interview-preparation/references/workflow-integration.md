# Workflow Integration: Interview Preparation

This document describes how `interview-preparation` integrates with other skills in the Career Development ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `cv-resume-builder` | **Upstream** | Resume stories to expand |
| `portfolio-presentation` | **Upstream** | Work examples to discuss |
| `brand-guidelines` | **Upstream** | Consistent messaging |
| `networking-outreach` | **Upstream** | Company intel from network |

## Prerequisites

Before invoking `interview-preparation`, ensure:

1. **Interview scheduled** - Date, format, interviewers known
2. **Job description available** - Role requirements clear
3. **Company researched** - Culture, challenges, news

## Handoff Patterns

### From: cv-resume-builder

**Trigger:** Resume led to interview.

**What to receive:**
- Resume content
- Key bullet points to expand
- Potential question areas
- Gaps to address proactively

**Integration points:**
- Prepare stories for each bullet
- Practice gap-bridging responses
- Anticipate "walk me through" questions

### From: portfolio-presentation

**Trigger:** Need specific examples.

**What to receive:**
- Project details and context
- Impact metrics
- Challenge/solution narratives
- Visuals for case presentations

**Integration points:**
- STAR/CAR story development
- Technical deep-dive preparation
- Whiteboard/case study practice

### From: brand-guidelines

**Trigger:** Ensure consistent narrative.

**What to receive:**
- Elevator pitch
- Value proposition
- Tone and language
- Key themes to emphasize

**Integration points:**
- "Tell me about yourself" answer
- Consistent messaging throughout
- Closing pitch preparation

### From: networking-outreach

**Trigger:** Gather company intelligence.

**What to receive:**
- Insider perspective
- Interview process details
- Team culture information
- Current challenges

**Integration points:**
- Informed questions to ask
- Cultural fit demonstration
- Challenge-specific examples

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Interview Preparation                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. UPSTREAM CONTEXT GATHERING                             │
│           │                                                 │
│           ├─────────────┬─────────────┬─────────────┐       │
│           ▼             ▼             ▼             ▼       │
│      CV-RESUME      PORTFOLIO      BRAND        NETWORK    │
│      BUILDER       PRESENTATION   GUIDELINES    OUTREACH   │
│           │             │             │             │       │
│           └─────────────┴─────────────┴─────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  2. INTERVIEW-PREPARATION: Build story bank and practice   │
│           │                                                 │
│           ▼                                                 │
│  3. Execute interview and gather feedback                  │
│           │                                                 │
│           ▼                                                 │
│  4. Feed learnings back to PORTFOLIO and BRAND             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing interview prep, verify:

- [ ] STAR stories prepared for key experiences
- [ ] "Tell me about yourself" refined and timed
- [ ] Technical concepts reviewed
- [ ] Company research complete
- [ ] Questions to ask prepared
- [ ] Logistics confirmed (time, location/link)
- [ ] Mock interview completed
- [ ] Salary expectations researched

## Common Scenarios

### Technical Interview

1. **Portfolio Presentation:** Technical project deep dives
2. **Interview Preparation:** Coding/system design practice
3. **CV Resume Builder:** Technical skills emphasis

### Behavioral Interview

1. **Portfolio Presentation:** STAR story examples
2. **Brand Guidelines:** Consistent narrative
3. **Interview Preparation:** Story practice and timing

### Executive Interview

1. **Brand Guidelines:** Executive presence
2. **Networking Outreach:** Leadership intel
3. **Interview Preparation:** Strategic conversation prep

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No preparation | Obvious and weak | Always research and practice |
| Scripted answers | Sounds robotic | Practice concepts, not scripts |
| No questions | Seems uninterested | Prepare thoughtful questions |
| Ignoring feedback | Repeat mistakes | Learn from each interview |

## Related Resources

- [Career Development Skills Ecosystem Map](../../../docs/guides/career-development-skills-ecosystem.md)
