# Roadmap Governance Protocols

Operational procedures for maintaining a living GitHub Projects roadmap.

## Weekly Cadence

### Monday Morning Protocol

**When**: Every Monday, first 30 minutes
**Who**: Product owner (required), tech lead (optional)

```
Checklist:
[ ] Review all items with Status = "In Progress"
[ ] Update Confidence levels
[ ] Check for stale items (no update in 14 days)
[ ] Update Target Ship Dates if needed
[ ] Log any slips in changelog
[ ] Review upcoming week's priorities
```

**Key Questions**:
- Did anything slip last week?
- Are confidence levels still accurate?
- Are any items blocked?

### Triage Protocol

**When**: Weekly, dedicated 30-minute session
**Who**: Product owner + relevant stakeholders

```
Triage Decision Tree:

New Issue Arrives
      │
      ▼
  Is it a bug?
      │
  ┌───┴───┐
  │       │
 Yes      No
  │       │
  ▼       ▼
Severity?  Strategic fit?
  │            │
  ▼            ▼
Critical   Backlog or
= Urgent   Reject
  │
Others
= Backlog

Outcome: Every item exits Triage with Status assigned
```

**Triage Outcomes**:
| Decision | Status Change | Notes |
|----------|---------------|-------|
| Accept | Triage → Backlog | Aligned, not urgent |
| Accept (urgent) | Triage → In Progress | Critical bug or business need |
| Defer | Triage → Backlog | Add "deferred" label, review in 30 days |
| Reject | Close issue | Explain why, link alternatives |
| Need Info | Keep in Triage | Assign owner to gather info |

---

## Health Metrics

### Say/Do Ratio

**Definition**: Percentage of items shipped in their target quarter

```
Calculation:
Say/Do Ratio = (Items shipped on time) / (Items committed for quarter) × 100

Target: >= 80%

< 60% = Planning problem
60-80% = Execution challenges
> 80% = Healthy roadmap
```

**Measurement**:
```
At quarter end:
1. Filter: Target Ship Date within quarter
2. Filter: Confidence = High (at quarter start)
3. Count: Status = Done
4. Calculate ratio
```

### Orphan Items

**Definition**: Roadmap initiatives not linked to execution issues

```
Detection Query:
- Item type = Initiative
- Linked issues = 0
- Status = In Progress

Action: All initiatives must have at least one linked execution issue
```

### Stale Items

**Definition**: Items in active status without recent updates

```
Stale Thresholds:
- In Progress: No update in 14 days
- Design: No update in 21 days
- Backlog (high priority): No update in 30 days

Detection:
- Filter: Status = In Progress
- Filter: Updated < (today - 14 days)
- Label as "Stale"
```

---

## Automation Rules

### In-Progress Trigger

**Trigger**: Branch created with issue reference
**Action**: Move issue to "In Progress"

```yaml
name: Auto In-Progress
on:
  create:
    branches:
      - 'feature/*'
      - 'fix/*'

jobs:
  update-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Extract issue number
        # Parse branch name for issue reference
      - name: Update project item
        # Move to In Progress status
```

### Stale Sweeper

**Trigger**: Daily at 9am
**Action**: Label stale items, notify owners

```yaml
name: Stale Detection
on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  check-stale:
    steps:
      - name: Find stale items
        # Query items not updated in threshold period
      - name: Add stale label
      - name: Notify in Slack/issue comment
```

### Done Trigger

**Trigger**: PR merged to main
**Action**: Move linked issues to "Done"

```yaml
name: Auto Done
on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  close-issues:
    if: github.event.pull_request.merged == true
    steps:
      - name: Update linked issues
        # Move to Done status in project
```

---

## WIP Limits

### Enforcement Rules

| Status | Per-Person Limit | Team Limit |
|--------|------------------|------------|
| In Progress | 2 | 6 |
| Design | 1 | 3 |
| Validation | - | 4 |

### When Limit Exceeded

```
1. Notify in daily standup
2. Identify cause:
   - Blocked item? → Escalate
   - Context switching? → Defer new work
   - Underestimated? → Replan
3. Restore limits before taking new work
```

---

## Reporting Templates

### Weekly Status Email

```markdown
# Roadmap Update: Week of [Date]

## Shipped This Week
- [Item]: [Brief outcome]

## In Progress
- [Item]: [Status, any blockers]

## Confidence Changes
- [Item]: High → Medium (reason)

## Coming Up
- [Item]: Starting next week

## Blockers
- [Item]: Blocked on [dependency]
```

### Quarterly Review

```markdown
# Q[X] Roadmap Review

## Say/Do Ratio: [X]%

## Shipped
| Initiative | Target | Actual | Notes |
|------------|--------|--------|-------|
| [Name] | [Date] | [Date] | [On time/Late] |

## Slipped
| Initiative | Original | New Target | Reason |
|------------|----------|------------|--------|

## Learnings
- [Learning 1]
- [Learning 2]

## Q[X+1] Priorities
1. [Theme]: [Focus area]
2. [Theme]: [Focus area]
```

---

## Shadow Items Pattern

For public roadmaps synced from private repositories.

### When to Use

- Public-facing roadmap for transparency
- Internal tracking with sensitive details
- Different audiences need different views

### Structure

```
Private Repo (Internal)
├── Issue #123: [Full details, technical notes]
│   └── Links to: Public Issue #45
│
Public Repo (External)
├── Issue #45: [Sanitized description]
    └── Labels: roadmap, public
```

### Sync Rules

| Private Field | Public Field | Sync |
|---------------|--------------|------|
| Title | Title (sanitized) | Manual |
| Status | Status | Automated |
| Target Date | Target Quarter | Manual |
| Technical Details | - | Never |
| Confidence | - | Never |

### Automation Caution

- Never auto-sync sensitive fields
- Review public items before status updates
- Use webhook with approval step
