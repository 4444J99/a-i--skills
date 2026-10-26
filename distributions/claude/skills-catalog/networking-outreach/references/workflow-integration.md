# Workflow Integration: Networking Outreach

This document describes how `networking-outreach` integrates with other skills in the Career Development ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `brand-guidelines` | **Upstream** | Receive messaging framework |
| `portfolio-presentation` | **Upstream** | Receive work to share |
| `cv-resume-builder` | **Complementary** | Resume for referrals |
| `interview-preparation` | **Downstream** | Connections lead to interviews |

## Prerequisites

Before invoking `networking-outreach`, ensure:

1. **Goals defined** - What you want from networking
2. **Target audience identified** - Who you want to connect with
3. **Value proposition clear** - What you offer

## Handoff Patterns

### From: brand-guidelines

**Trigger:** Brand messaging ready for outreach.

**What to receive:**
- Elevator pitch
- Key talking points
- Professional voice
- Value proposition

**Integration points:**
- LinkedIn summary and messages
- Introduction scripts
- Follow-up communications

### From: portfolio-presentation

**Trigger:** Work ready to share.

**What to receive:**
- Portfolio URL
- Selected projects to highlight
- Talking points for each
- Context for different audiences

**Integration points:**
- Sharing in conversations
- Post content for visibility
- Discussion starters

### To: cv-resume-builder

**Trigger:** Connection requests resume.

**What to hand off:**
- Connection context
- Specific opportunity
- Tailoring requirements

**Expected output from resume:**
- Targeted resume version
- Cover letter if needed
- Application package

### To: interview-preparation

**Trigger:** Networking leads to interview.

**What to hand off:**
- Company insider context
- Hiring manager insights
- Team information
- Interview process details

**Expected output from interview prep:**
- Informed preparation
- Insider-aware responses
- Relevant questions

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Networking Workflow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. BRAND-GUIDELINES: Define messaging and pitch           │
│           │                                                 │
│           ▼                                                 │
│  2. PORTFOLIO-PRESENTATION: Prepare work to share          │
│           │                                                 │
│           ▼                                                 │
│  3. NETWORKING-OUTREACH: Execute outreach strategy         │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. CV-RESUME-BUILDER         4b. INTERVIEW-PREPARATION   │
│      (when resume requested)       (when interview set)    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing outreach, verify:

- [ ] Clear ask or purpose
- [ ] Personalized message (not generic)
- [ ] Value offered, not just requested
- [ ] Follow-up plan in place
- [ ] LinkedIn profile updated
- [ ] Portfolio ready to share
- [ ] Tracking system for contacts
- [ ] Thank you notes prepared

## Common Scenarios

### Job Search Networking

1. **Brand Guidelines:** Positioning for target role
2. **Portfolio Presentation:** Relevant work selected
3. **Networking Outreach:** Targeted connections
4. **Interview Preparation:** Leverage network intel

### Industry Event Networking

1. **Brand Guidelines:** Elevator pitch
2. **Portfolio Presentation:** Portable examples
3. **Networking Outreach:** Pre-event research

### Warm Introduction Request

1. **Networking Outreach:** Craft introduction request
2. **CV Resume Builder:** Resume for sharing
3. **Brand Guidelines:** Consistent follow-up

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Mass generic outreach | Low response rate | Personalize each message |
| Only ask, never give | One-sided relationship | Offer value first |
| No follow-up | Connections fade | Systematic follow-up |
| Neglecting weak ties | Missing opportunities | Nurture broad network |

## Related Resources

- [Career Development Skills Ecosystem Map](../../../docs/guides/career-development-skills-ecosystem.md)
