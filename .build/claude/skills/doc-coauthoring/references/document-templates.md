# Document Type Templates

Templates for common document types used in the co-authoring workflow.

---

## Technical Specification

```markdown
# [Feature/System Name] Technical Specification

## Overview

**Status**: Draft | In Review | Approved
**Author**: [Name]
**Reviewers**: [Names]
**Last Updated**: [Date]

### Summary
[2-3 sentences describing what this spec covers]

### Goals
- [Goal 1]
- [Goal 2]

### Non-Goals
- [What this explicitly does NOT cover]

---

## Background

### Context
[Why is this needed? What problem does it solve?]

### Current State
[How things work today]

### Requirements
| Requirement | Priority | Source |
|-------------|----------|--------|
| [Req 1]     | Must Have | [Stakeholder] |
| [Req 2]     | Should Have | [User Research] |

---

## Technical Design

### Architecture Overview
[High-level system diagram or description]

### Components
#### [Component 1]
- **Purpose**: [What it does]
- **Interface**: [How it communicates]
- **Dependencies**: [What it relies on]

### Data Model
[Schema, data structures, storage]

### API Design
[Endpoints, contracts, protocols]

---

## Implementation Plan

### Phases
| Phase | Description | Duration | Dependencies |
|-------|-------------|----------|--------------|
| 1     | [Phase 1]   | [Time]   | [Deps]       |

### Milestones
- [ ] [Milestone 1]
- [ ] [Milestone 2]

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |

---

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

---

## Appendix
[Additional technical details, diagrams, references]
```

---

## Decision Document (ADR)

```markdown
# [Decision Title]

## Status
Proposed | Accepted | Deprecated | Superseded by [ADR-XXX]

## Context
[What is the situation that requires a decision? What constraints exist?]

## Decision Drivers
- [Driver 1: e.g., performance requirements]
- [Driver 2: e.g., team expertise]
- [Driver 3: e.g., maintenance burden]

## Considered Options
1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome
**Chosen Option**: [Option X]

**Rationale**: [Why this option best addresses the drivers]

### Positive Consequences
- [Benefit 1]
- [Benefit 2]

### Negative Consequences
- [Tradeoff 1]
- [Tradeoff 2]

## Options Analysis

### Option 1: [Name]
**Description**: [How it works]

| Pros | Cons |
|------|------|
| [Pro 1] | [Con 1] |

### Option 2: [Name]
**Description**: [How it works]

| Pros | Cons |
|------|------|
| [Pro 1] | [Con 1] |

## Related Decisions
- [Link to related ADR]
- [Link to related spec]
```

---

## Product Requirements Document (PRD)

```markdown
# [Product/Feature Name] PRD

## Document Info
| Field | Value |
|-------|-------|
| Owner | [PM Name] |
| Status | Draft / In Review / Approved |
| Target Release | [Quarter/Date] |
| Last Updated | [Date] |

---

## Executive Summary
[One paragraph explaining what we're building and why]

## Problem Statement
### User Pain Points
- [Pain point 1]
- [Pain point 2]

### Business Impact
- [Current state metric]
- [Desired outcome]

## Goals & Success Metrics

| Goal | Metric | Target | Measurement |
|------|--------|--------|-------------|
| [Goal 1] | [KPI] | [Target] | [How measured] |

---

## User Stories

### Persona: [User Type]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Requirements

### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | [Requirement] | P0/P1/P2 | [Notes] |

### Non-Functional Requirements
| Category | Requirement |
|----------|-------------|
| Performance | [Latency, throughput targets] |
| Scalability | [Load expectations] |
| Security | [Compliance, auth requirements] |
| Accessibility | [WCAG level] |

---

## Scope

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Item 1] (reason)
- [Item 2] (deferred to Phase 2)

---

## Dependencies
| Dependency | Team/System | Status | Risk |
|------------|-------------|--------|------|
| [Dep 1]    | [Team]      | [Status] | [Risk level] |

---

## Timeline
| Milestone | Date | Owner |
|-----------|------|-------|
| Design Complete | [Date] | [Name] |
| Dev Complete | [Date] | [Name] |
| Launch | [Date] | [Name] |

---

## Appendix
- [Mockups/Wireframes]
- [User Research]
- [Competitive Analysis]
```

---

## Request for Comments (RFC)

```markdown
# RFC: [Proposal Title]

## Metadata
- **Authors**: [Names]
- **Status**: Draft | Open for Comments | Final
- **Created**: [Date]
- **Comment Period Ends**: [Date]

---

## Summary
[One paragraph explaining the proposal]

## Motivation
### Current Problem
[What's broken or missing?]

### Why Now?
[Why is this the right time to address this?]

---

## Proposal

### High-Level Overview
[Conceptual explanation]

### Detailed Design
[Technical or process details]

### Alternatives Considered
| Alternative | Why Not Chosen |
|-------------|----------------|
| [Alt 1]     | [Reason]       |

---

## Impact Analysis

### Who is Affected?
- [Team/User group 1]
- [Team/User group 2]

### Migration Path
[How do we get from current state to proposed state?]

### Backward Compatibility
[Impact on existing systems/processes]

---

## Open Questions
- [ ] [Question for reviewers]

## Action Items
- [ ] [Post-approval action]

---

## Feedback
[This section filled during comment period]

### Comments Summary
| Commenter | Feedback | Resolution |
|-----------|----------|------------|
| [Name]    | [Comment] | [How addressed] |
```

---

## Usage Tips

### Choosing the Right Template

| Document Type | Use When |
|---------------|----------|
| Technical Spec | Building a system or feature with significant engineering |
| Decision Doc (ADR) | Choosing between technical approaches |
| PRD | Defining product requirements for cross-functional teams |
| RFC | Proposing changes that need broad input |

### Section Priority

For each document type, focus first on:

1. **Technical Spec**: Requirements and Architecture
2. **Decision Doc**: Options Analysis and Rationale
3. **PRD**: Problem Statement and User Stories
4. **RFC**: Motivation and Impact Analysis
