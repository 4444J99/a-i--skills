# GitHub Projects Field Taxonomy

Reference guide for custom fields in GitHub Projects V2 roadmap systems.

## Core Field Definitions

### Status Field

The primary workflow field. All items must have a status.

| Status | Definition | Automation Trigger |
|--------|------------|-------------------|
| **Triage** | New, unreviewed items | Default for all new issues |
| **Backlog** | Reviewed, not committed | Manual after triage |
| **Design** | Spec/design in progress | Manual or linked PR |
| **In Progress** | Active development | Branch created |
| **Validation** | Testing/review phase | PR opened |
| **Done** | Shipped and verified | PR merged to main |

### Strategic Theme Field

Categorizes items by business objective. Review quarterly.

| Theme | Description | Example Items |
|-------|-------------|---------------|
| **User Growth** | Acquisition and activation | Onboarding, referrals |
| **Retention** | Reduce churn, increase engagement | Notifications, features |
| **Revenue** | Monetization improvements | Pricing, upsells |
| **Tech Debt** | Infrastructure and stability | Refactoring, upgrades |
| **Platform** | Foundation for future features | APIs, architecture |
| **Compliance** | Legal and security requirements | GDPR, SOC2 |

### Confidence Field

Reflects certainty of delivery. Update weekly.

| Level | Definition | Action |
|-------|------------|--------|
| **High** | Clear scope, team assigned, no blockers | Commit to stakeholders |
| **Medium** | Scope defined, some uncertainty | Plan contingencies |
| **Low** | High uncertainty, dependencies unknown | Do not communicate externally |

### Target Ship Date

Distinct from engineering iteration. Represents external commitment.

- Format: `YYYY-MM-DD` or quarter (`2024-Q2`)
- Update when confidence changes
- Never silently slip - always communicate changes

---

## Item Types

### Initiative (Roadmap-Level)

```
Fields Required:
- Title: [Theme] Brief outcome statement
- Status: Backlog through Done
- Theme: Strategic category
- Confidence: High/Medium/Low
- Target Ship Date: Committed date
- Owner: Product owner name
- Description: One-paragraph scope

Example:
Title: [User Growth] Streamlined onboarding flow
Theme: User Growth
Confidence: High
Target: 2024-Q2
Owner: @pm-name
```

### Feature (Execution-Level)

```
Fields Required:
- Title: Specific deliverable
- Parent Initiative: Linked initiative
- Status: Full workflow
- Points/Estimate: Engineering size
- Assignee: Developer

Example:
Title: Email verification step removal
Parent: Streamlined onboarding flow
Status: In Progress
Points: 5
Assignee: @dev-name
```

### Bug/Issue (Maintenance)

```
Fields Required:
- Title: Problem statement
- Severity: Critical/High/Medium/Low
- Status: Triage through Done
- Reported By: Source (user, internal, automated)

Severity Definitions:
- Critical: Production down, data loss
- High: Major feature broken
- Medium: Feature degraded
- Low: Cosmetic, edge case
```

---

## View Configurations

### Executive Timeline View

**Purpose**: Stakeholder communication

```
Type: Roadmap (Gantt)
Group by: Strategic Theme
Filter: Item type = Initiative
Sort: Target Ship Date (ascending)
Show fields: Title, Confidence, Target Ship Date
Date field: Target Ship Date
```

### Engineering Kanban View

**Purpose**: Daily development work

```
Type: Board
Columns: Status (all values)
Swimlanes: Assignee
Filter: Item type = Feature OR Bug
Show fields: Title, Points, Labels
WIP Limits: In Progress <= 2 per person
```

### Triage Queue View

**Purpose**: Weekly review session

```
Type: Table
Filter: Status = Triage
Sort: Created date (oldest first)
Show fields: Title, Created, Reported By, Labels
```

### Theme Summary View

**Purpose**: Portfolio balance review

```
Type: Table
Group by: Strategic Theme
Filter: Status != Done
Show fields: Title, Confidence, Target Ship Date
Summary: Count per theme
```

---

## Field Naming Conventions

### Consistent Naming

| Good | Bad |
|------|-----|
| `Status` | `State`, `Phase` |
| `Strategic Theme` | `Category`, `Type` |
| `Target Ship Date` | `Due Date`, `Deadline` |
| `Confidence` | `Certainty`, `Risk` |

### Field Types

| Field | Type | Why |
|-------|------|-----|
| Status | Single select | Enforces workflow |
| Theme | Single select | Clean grouping |
| Confidence | Single select | Limited options |
| Target Ship Date | Date | Gantt compatibility |
| Points | Number | Calculations |
| Owner | Text | Flexibility |

---

## Migration Checklist

When setting up a new roadmap:

- [ ] Create project with V2 layout
- [ ] Add Status field with all values
- [ ] Add Strategic Theme field
- [ ] Add Confidence field
- [ ] Add Target Ship Date field
- [ ] Create Executive Timeline view
- [ ] Create Engineering Kanban view
- [ ] Create Triage Queue view
- [ ] Set up automation rules
- [ ] Document field definitions for team
- [ ] Schedule weekly triage meeting

---

## Anti-Patterns

### Field Proliferation

**Problem**: Too many custom fields
**Solution**: Start minimal, add only when needed

### Status Overload

**Problem**: 10+ status values
**Solution**: Max 6 statuses, use labels for subtypes

### Theme Creep

**Problem**: Themes become catch-all buckets
**Solution**: Review themes quarterly, merge or split

### Date Confusion

**Problem**: Target date vs sprint vs actual ship
**Solution**: One date field per purpose, clear naming
