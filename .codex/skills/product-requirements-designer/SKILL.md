---
name: product-requirements-designer
description: Comprehensive product requirements documentation from problem definition through launch planning. Supports both enterprise PRD (full specs, cross-functional alignment) and lean/startup style (hypothesis-driven one-pagers). Framework-agnostic with templates for Agile, Jobs-to-Be-Done, and hybrid approaches. Scaffolds related artifacts including user stories, acceptance criteria, wireframes brief, and technical handoff specs. Triggers on PRD creation, product specs, feature requirements, or product design documentation.
---

# Product Requirements Designer

Transform product vision into actionable specifications.

## Mode Selection

### Document Scope

**Enterprise PRD**: Full cross-functional specification
- Complete problem analysis with market context
- Detailed functional and non-functional requirements
- Success metrics with measurement plans
- Risk assessment and mitigation
- Full launch and rollout plan
- Stakeholder sign-off sections

**Lean PRD**: Hypothesis-driven one-pager
- Problem/opportunity statement
- Proposed solution with key assumptions
- MVP scope and success criteria
- Learning goals and experiment design
- Quick iteration plan

### Framework Selection

**Agile/Scrum**: Epics → Features → User Stories → Acceptance Criteria

**Jobs-to-Be-Done**: Job statement → Forces diagram → Solution mapping

**Outcome-Driven**: Desired outcomes → Opportunity scoring → Solution requirements

**Hybrid**: Mix frameworks based on product stage and team needs

---

## Enterprise PRD Structure

### 1. Executive Summary
- Product/feature name
- One-paragraph description
- Primary stakeholders
- Target release
- Document status and version

### 2. Problem Definition

#### 2.1 Problem Statement
```
[User type] experiences [problem] when trying to [goal], 
which results in [negative outcome].
```

#### 2.2 Evidence
| Evidence Type | Source | Finding |
|---------------|--------|---------|
| User research | [Study/interviews] | [Key insight] |
| Analytics | [Data source] | [Metric showing problem] |
| Support data | [Tickets/feedback] | [Pattern identified] |
| Market research | [Source] | [Competitive gap] |

#### 2.3 Impact of Not Solving
- Business impact: [Revenue, churn, efficiency]
- User impact: [Frustration, abandonment, workarounds]
- Strategic impact: [Market position, competitive threat]

### 3. Goals and Success Metrics

#### 3.1 Business Goals
| Goal | Metric | Current | Target | Timeline |
|------|--------|---------|--------|----------|
| [Goal] | [KPI] | [Baseline] | [Target] | [By when] |

#### 3.2 User Goals
| User Segment | Goal | Success Indicator |
|--------------|------|-------------------|
| [Segment] | [What they want to achieve] | [How we know they succeeded] |

#### 3.3 Success Metrics (HEART Framework)
- **Happiness**: [User satisfaction measure]
- **Engagement**: [Usage depth measure]
- **Adoption**: [New user/feature uptake]
- **Retention**: [Return usage measure]
- **Task Success**: [Completion rate, time, errors]

### 4. User Analysis

#### 4.1 Target Users
| Persona | Description | Primary Need | Usage Context |
|---------|-------------|--------------|---------------|
| [Name] | [Who they are] | [Core need] | [When/where/how] |

#### 4.2 User Journey (Current State)
```
[Trigger] → [Step 1] → [Pain Point] → [Step 2] → [Pain Point] → [Outcome]
```

#### 4.3 User Journey (Future State)
```
[Trigger] → [Improved Step 1] → [Step 2] → [Desired Outcome]
```

### 5. Solution Overview

#### 5.1 Proposed Solution
[High-level description of what we're building]

#### 5.2 Key Capabilities
1. [Capability 1]: [What it enables]
2. [Capability 2]: [What it enables]
3. [Capability 3]: [What it enables]

#### 5.3 Solution Principles
- [Principle 1]: [Why it matters]
- [Principle 2]: [Why it matters]

#### 5.4 Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

### 6. Detailed Requirements

#### 6.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| FR-001 | [System shall...] | P0/P1/P2 | [Why needed] |
| FR-002 | [System shall...] | P0/P1/P2 | [Why needed] |

**Priority Definitions**:
- P0: Must have for launch (blocking)
- P1: Should have for launch (significant value)
- P2: Nice to have (incremental value)

#### 6.2 Non-Functional Requirements

| Category | Requirement | Target | Rationale |
|----------|-------------|--------|-----------|
| Performance | [Response time, throughput] | [Specific target] | [Why] |
| Scalability | [Load, growth capacity] | [Specific target] | [Why] |
| Security | [Auth, data protection] | [Standard/compliance] | [Why] |
| Accessibility | [WCAG level, devices] | [Specific target] | [Why] |
| Reliability | [Uptime, recovery] | [Specific target] | [Why] |

#### 6.3 Constraints
- Technical: [Platform, integration, legacy constraints]
- Business: [Budget, timeline, resource constraints]
- Regulatory: [Compliance, legal constraints]

### 7. User Experience

#### 7.1 UX Principles for This Feature
1. [Principle]: [Application]
2. [Principle]: [Application]

#### 7.2 Key Interactions
| Interaction | User Action | System Response | Success State |
|-------------|-------------|-----------------|---------------|
| [Name] | [What user does] | [What happens] | [Result] |

#### 7.3 Edge Cases and Error States
| Scenario | Handling | User Message |
|----------|----------|--------------|
| [Edge case] | [How handled] | [What user sees] |

### 8. Technical Considerations

#### 8.1 Architecture Impact
- [System/component affected]: [Type of change]

#### 8.2 Dependencies
| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| [System/API/Team] | Blocking/Informational | [Who] | [Status] |

#### 8.3 Data Requirements
- New data entities: [List]
- Data migrations: [Required/Not required]
- Privacy considerations: [PII handling, retention]

#### 8.4 Integration Points
| System | Integration Type | Data Flow |
|--------|------------------|-----------|
| [System] | [API/Event/Batch] | [In/Out/Bidirectional] |

### 9. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [Mitigation plan] |

### 10. Launch Plan

#### 10.1 Rollout Strategy
- [ ] Internal dogfood: [Date]
- [ ] Beta/Limited release: [Date, criteria]
- [ ] General availability: [Date]

#### 10.2 Feature Flags
| Flag | Purpose | Default | Rollout Plan |
|------|---------|---------|--------------|
| [Flag name] | [What it controls] | Off/On | [% ramp plan] |

#### 10.3 Success Criteria for Each Phase
| Phase | Success Criteria | Go/No-Go Decision |
|-------|------------------|-------------------|
| Beta | [Criteria] | [Who decides] |
| GA | [Criteria] | [Who decides] |

#### 10.4 Rollback Plan
[Conditions and process for rollback]

### 11. Cross-Functional Requirements

#### 11.1 Marketing
- Positioning: [Key message]
- Launch activities: [Required support]

#### 11.2 Sales/CS
- Training needs: [What teams need to know]
- Documentation: [Customer-facing docs needed]

#### 11.3 Legal/Compliance
- Reviews required: [List]
- Approvals needed: [List]

### 12. Timeline and Milestones

| Milestone | Date | Owner | Dependencies |
|-----------|------|-------|--------------|
| PRD approved | [Date] | [PM] | Stakeholder review |
| Design complete | [Date] | [Design] | PRD |
| Dev complete | [Date] | [Eng] | Design |
| QA complete | [Date] | [QA] | Dev |
| Launch | [Date] | [PM] | All |

### 13. Open Questions

| Question | Owner | Due Date | Status |
|----------|-------|----------|--------|
| [Question] | [Who answers] | [When] | Open/Resolved |

### 14. Appendix

- A: User Research Summary
- B: Competitive Analysis
- C: Technical Design Doc (link)
- D: Design Specs (link)

### 15. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product | | | |
| Engineering | | | |
| Design | | | |
| [Other stakeholders] | | | |

---

## Lean PRD Structure (One-Pager)

### Header
**Feature**: [Name]  
**Owner**: [PM]  
**Date**: [Date]  
**Status**: Draft/In Review/Approved

### Problem
[2-3 sentences: Who has the problem, what is it, why does it matter]

### Hypothesis
```
We believe that [solution/change]
for [user segment]
will achieve [outcome]
We will know this is true when [measurable signal]
```

### Proposed Solution
[Brief description with key capabilities—keep to 3-5 bullets]

### Key Assumptions
| Assumption | Risk if Wrong | How to Validate |
|------------|---------------|-----------------|
| [Assumption] | [Impact] | [Test/signal] |

### MVP Scope
**In**: [Minimum features for learning]
**Out**: [Explicitly deferred]

### Success Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Primary metric] | [Target] | [How measured] |
| [Secondary metric] | [Target] | [How measured] |

### Timeline
- Build: [Duration]
- Learn: [Duration]
- Decide: [Date for go/no-go]

### Resources Needed
- Engineering: [Estimate]
- Design: [Estimate]
- Other: [Estimate]

### Risks and Mitigations
[Top 2-3 risks with mitigations]

### Next Steps
1. [Immediate next action]
2. [Following action]

---

## Framework-Specific Templates

### Agile: Epic Template
See `references/agile-templates.md`

### Jobs-to-Be-Done: Job Map Template  
See `references/jtbd-templates.md`

### Outcome-Driven: Opportunity Template
See `references/odi-templates.md`

---

## Related Artifacts

This skill scaffolds the following artifacts alongside the PRD:

### User Stories
See `references/user-stories-template.md`

### Acceptance Criteria
See `references/acceptance-criteria-template.md`

### Wireframes Brief
See `references/wireframes-brief-template.md`

### Technical Handoff Spec
See `references/technical-handoff-template.md`

---

## Workflow

### Discovery Phase
1. Problem validation → Evidence gathering → Opportunity sizing

### Definition Phase
2. Solution framing → Requirements drafting → Stakeholder alignment

### Specification Phase
3. Detailed requirements → UX specs → Technical specs

### Alignment Phase
4. Cross-functional review → Risk assessment → Sign-off

### Handoff Phase
5. Artifact scaffolding → Team briefing → Kickoff

---

## References

- `references/agile-templates.md` - Epic, feature, story templates
- `references/jtbd-templates.md` - Job statement, forces diagram
- `references/odi-templates.md` - Outcome-driven innovation templates
- `references/user-stories-template.md` - User story formats
- `references/acceptance-criteria-template.md` - AC patterns
- `references/wireframes-brief-template.md` - Design handoff brief
- `references/technical-handoff-template.md` - Engineering handoff spec
