# Agile Templates

## Epic Template

### Epic Header
```
EPIC: [EPIC-XXX] [Epic Name]
Owner: [Product Owner]
Status: Draft | Refined | Ready | In Progress | Done
Target Release: [Version/Quarter]
```

### Epic Description

**Vision Statement**
```
FOR [target user]
WHO [has need/problem]
THE [product/feature name]
IS A [product category]
THAT [key benefit/value]
UNLIKE [current alternative]
OUR SOLUTION [key differentiator]
```

**Background**
[Context and motivation for this epic—why now, what changed]

**Goals**
- [ ] [Goal 1 with measurable outcome]
- [ ] [Goal 2 with measurable outcome]

**Non-Goals**
- [Explicitly out of scope item]

### Success Metrics
| Metric | Baseline | Target | Method |
|--------|----------|--------|--------|
| [KPI] | [Current] | [Goal] | [How measured] |

### Features (Child Items)
| ID | Feature | Priority | Status | Points |
|----|---------|----------|--------|--------|
| [FEAT-001] | [Feature name] | P0/P1/P2 | [Status] | [Est] |
| [FEAT-002] | [Feature name] | P0/P1/P2 | [Status] | [Est] |

### Dependencies
| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| [Item] | Blocks/Blocked by | [Team] | [Status] |

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Plan] |

### Timeline
| Milestone | Target Date | Actual | Notes |
|-----------|-------------|--------|-------|
| Refinement complete | [Date] | | |
| Sprint 1 start | [Date] | | |
| MVP complete | [Date] | | |
| Full release | [Date] | | |

---

## Feature Template

### Feature Header
```
FEATURE: [FEAT-XXX] [Feature Name]
Parent Epic: [EPIC-XXX]
Owner: [PM/Lead]
Status: Draft | Refined | Ready | In Progress | Done
```

### Description
**Summary**: [One sentence description]

**User Value**: [Why users want this]

**Business Value**: [Why business wants this]

### Acceptance Criteria (Feature Level)
- [ ] [High-level criterion 1]
- [ ] [High-level criterion 2]
- [ ] [High-level criterion 3]

### User Stories
| ID | Story | Points | Status |
|----|-------|--------|--------|
| [US-001] | As a [user], I want [goal] so that [benefit] | [Est] | [Status] |
| [US-002] | As a [user], I want [goal] so that [benefit] | [Est] | [Status] |

### UX Notes
[Key interaction patterns, wireframe links, design considerations]

### Technical Notes
[Architecture considerations, tech debt, dependencies]

### Out of Scope
- [Deferred item 1]
- [Deferred item 2]

---

## User Story Template

### Story Header
```
STORY: [US-XXX] [Story Title]
Parent Feature: [FEAT-XXX]
Status: Draft | Refined | Ready | In Progress | Done
Points: [Estimate]
```

### Story Statement
```
AS A [user type/persona]
I WANT [goal/desire]
SO THAT [benefit/value]
```

### Context
[Additional context, background, or constraints]

### Acceptance Criteria
```gherkin
GIVEN [precondition/context]
WHEN [action/trigger]
THEN [expected outcome]
AND [additional outcome]
```

**Criteria Checklist**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Definition of Done
- [ ] Code complete and reviewed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Acceptance criteria verified
- [ ] Documentation updated
- [ ] Product owner accepted

### Design Assets
- Wireframes: [Link]
- Mockups: [Link]
- Prototype: [Link]

### Technical Notes
- Implementation approach: [Notes]
- APIs affected: [List]
- Database changes: [Y/N, details]

### Test Scenarios
| Scenario | Steps | Expected Result |
|----------|-------|-----------------|
| Happy path | [Steps] | [Result] |
| Edge case 1 | [Steps] | [Result] |
| Error case | [Steps] | [Result] |

---

## Sprint Planning Template

### Sprint Header
```
SPRINT: [Sprint Number/Name]
Dates: [Start] - [End]
Goal: [One sentence sprint goal]
Capacity: [Team points/hours]
```

### Sprint Goal
[Clear, measurable goal for the sprint]

### Committed Stories
| ID | Story | Points | Owner | Status |
|----|-------|--------|-------|--------|
| [US-XXX] | [Title] | [Pts] | [Dev] | [Status] |

### Sprint Capacity
| Team Member | Capacity | Allocated | Remaining |
|-------------|----------|-----------|-----------|
| [Name] | [Points] | [Points] | [Points] |

### Risks/Blockers
| Item | Risk/Blocker | Owner | Mitigation |
|------|--------------|-------|------------|
| [Item] | [Description] | [Who] | [Plan] |

### Carryover from Previous Sprint
| ID | Story | Original Points | Notes |
|----|-------|-----------------|-------|
| [US-XXX] | [Title] | [Pts] | [Why carried] |

---

## Backlog Refinement Template

### Session Info
```
Date: [Date]
Attendees: [List]
Items Refined: [Count]
```

### Items Refined
| ID | Item | Before | After | Notes |
|----|------|--------|-------|-------|
| [ID] | [Title] | [Old estimate] | [New estimate] | [Key decisions] |

### Questions Raised
| Question | Owner | Due | Status |
|----------|-------|-----|--------|
| [Question] | [Who] | [When] | [Status] |

### Items Needing More Refinement
| ID | Item | Missing Info | Next Steps |
|----|------|--------------|------------|
| [ID] | [Title] | [What's needed] | [Action] |

### Action Items
- [ ] [Action] - [Owner] - [Due]
