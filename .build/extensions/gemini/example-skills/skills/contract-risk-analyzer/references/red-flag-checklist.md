# Contract Red Flag Checklist

Quick reference for identifying high-risk contract clauses.

## Payment Terms Red Flags

### Dangerous Patterns

| Issue | Red Flag Language | Recommended Alternative |
|-------|-------------------|------------------------|
| Extended payment | "Net 90", "Net 120" | Net 30 or milestone-based |
| No late fees | Payment terms with no penalties | "1.5% monthly on overdue" |
| No kill fee | Silent on project cancellation | "50% kill fee on cancellation" |
| Vague milestones | "Upon completion" | Specific deliverable dates |
| Retainer abuse | "Unused hours do not roll over" | Hours roll over 90 days |

### Payment Checklist

- [ ] Payment terms are Net 30 or shorter
- [ ] Late payment penalties are specified (1-2% monthly)
- [ ] Kill fee / cancellation terms exist (25-50% of remaining)
- [ ] Milestone payments tied to specific deliverables
- [ ] Deposit required before work begins (25-50%)
- [ ] Currency and payment method specified
- [ ] Who covers transaction fees is clear

---

## Scope & Deliverables Red Flags

### Dangerous Language

| Phrase | Risk | Counter Language |
|--------|------|------------------|
| "...and other duties as assigned" | Unlimited scope | Remove or specify duties |
| "Reasonable revisions" | Subjective, unlimited | "Up to 2 rounds of revisions" |
| "Until client satisfaction" | Never-ending project | Defined acceptance criteria |
| "Best efforts" | Vague performance standard | Specific deliverables |
| "Professional quality" | Subjective standard | Reference to spec document |

### Scope Checklist

- [ ] Deliverables explicitly listed (not "as discussed")
- [ ] Revision rounds capped (2-3 rounds typical)
- [ ] Acceptance criteria defined (timeline, process)
- [ ] Out-of-scope work pricing method stated
- [ ] Change request process documented
- [ ] Timeline has buffer for client delays

---

## Intellectual Property Red Flags

### IP Ownership Comparison

| Clause Type | What You Keep | What Client Gets | When to Use |
|-------------|---------------|------------------|-------------|
| Work for Hire | Nothing | Full ownership | High payment, custom work |
| License (Exclusive) | Ownership | Exclusive use rights | Medium payment |
| License (Non-Exclusive) | Ownership | Shared use rights | Lower payment, reusable work |
| Retained Rights | Portfolio rights | Full ownership | Standard arrangement |

### Dangerous IP Language

```
"All work product, including preliminary sketches,
drafts, and materials, shall become the sole
property of Client upon creation."
```

**Risk:** You lose rights to everything, even unused concepts.

**Better:**

```
"Upon full payment, Client receives ownership of
final deliverables. Contractor retains rights to
preliminary work, portfolio use, and underlying
methodologies."
```

### IP Checklist

- [ ] "Work for hire" only if intentional and compensated
- [ ] Portfolio rights explicitly retained
- [ ] Pre-existing work/tools excluded from transfer
- [ ] Rights transfer only after full payment
- [ ] Underlying code/libraries remain yours
- [ ] Client indemnifies against third-party IP claims

---

## Liability & Indemnification Red Flags

### Dangerous Patterns

| Issue | Red Flag | Acceptable Alternative |
|-------|----------|------------------------|
| Unlimited liability | "Contractor shall indemnify Client against all claims" | Cap at contract value |
| Broad indemnity | "Any and all damages arising from" | Limit to contractor negligence |
| Warranty period | "Perpetual warranty" | 30-90 day warranty |
| Consequential damages | "Including lost profits" | Exclude consequential damages |
| Legal fee shifting | "Contractor pays all legal fees" | Mutual or prevailing party |

### Liability Checklist

- [ ] Total liability capped (1-2x contract value)
- [ ] Indemnification is mutual, not one-sided
- [ ] Indemnification limited to gross negligence/willful misconduct
- [ ] Consequential/indirect damages excluded
- [ ] Warranty period is reasonable (30-90 days)
- [ ] Force majeure clause included
- [ ] Insurance requirements are reasonable

---

## Non-Compete & Non-Solicitation Red Flags

### Reasonable vs. Unreasonable

| Factor | Unreasonable | Reasonable |
|--------|--------------|------------|
| Duration | 5 years | 6-12 months |
| Geography | Worldwide | Client's operating region |
| Scope | "Similar services" | Specific competing products |
| Industry | Entire industry banned | Direct competitors only |

### Non-Compete Checklist

- [ ] Duration is 6-12 months maximum
- [ ] Geographic scope is limited and specific
- [ ] Competing activities are narrowly defined
- [ ] Does not prevent working in your field
- [ ] Non-solicit (employees only) vs. non-compete
- [ ] Carve-out for existing clients/relationships

---

## Termination Red Flags

### Dangerous Patterns

| Issue | Red Flag | Acceptable Alternative |
|-------|----------|------------------------|
| Unilateral termination | "Client may terminate at any time" | Both parties, with notice |
| No payment on termination | Silent on partial work payment | Pro-rata payment for work done |
| Immediate termination | "Effective immediately" | 14-30 day notice period |
| No cure period | "Any breach = termination" | 10-day cure period for minor breaches |

### Termination Checklist

- [ ] Mutual termination rights (not just client)
- [ ] Notice period specified (14-30 days)
- [ ] Payment for completed work guaranteed
- [ ] Cure period for minor/non-material breaches
- [ ] Return of materials process defined
- [ ] Survival clauses are reasonable

---

## Quick Risk Assessment

### Contract Risk Score

Add up the red flags found:

| Score | Risk Level | Recommendation |
|-------|------------|----------------|
| 0-2 | Low | Sign with minor edits |
| 3-5 | Medium | Negotiate key issues |
| 6-8 | High | Major revision needed |
| 9+ | Critical | Walk away or full rewrite |

### Walk-Away Triggers

Recommend declining if any of these are non-negotiable:

1. Unlimited/uncapped liability
2. Perpetual non-compete in your industry
3. No payment for work on cancellation
4. Unlimited "work for hire" without premium
5. "Pay when we get paid" from agencies
6. No cure period with immediate termination rights
7. Client owns all work before payment
