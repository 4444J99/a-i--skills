# User Stories Template

## Story Formats

### Classic Format
```
As a [user type],
I want [goal/desire],
So that [benefit/value].
```

### Job Story Format (JTBD-influenced)
```
When [situation/context],
I want to [motivation],
So I can [expected outcome].
```

### Feature-Driven Format
```
[User type] can [capability]
so that [value delivered].
```

---

## Story Types

### Functional Stories
User-facing functionality that delivers direct value.

```
As a premium subscriber,
I want to download episodes for offline listening,
So that I can enjoy content during my commute without using data.
```

### Enabler Stories
Technical work that enables future functional stories.

```
As a development team,
We need to implement a caching layer,
So that we can support offline functionality.
```

### Spike Stories
Time-boxed research/exploration.

```
As a development team,
We need to investigate offline storage options,
So that we can estimate the download feature accurately.
Time-box: 2 days
Output: Recommendation document
```

---

## Story Sizing Guide

| Size | Points | Characteristics | Example |
|------|--------|-----------------|---------|
| XS | 1 | Config change, copy update | "Change button text" |
| S | 2 | Single component, clear path | "Add validation to form field" |
| M | 3 | Multiple components, some unknowns | "Build new filter component" |
| L | 5 | Cross-cutting, dependencies | "Implement search with filters" |
| XL | 8 | Consider splitting | "Build reporting dashboard" |
| XXL | 13+ | Must split | "Implement payment system" |

---

## Story Template (Full)

### Header
```
ID: [US-XXX]
Title: [Descriptive title]
Epic: [Parent epic]
Feature: [Parent feature]
Priority: [P0/P1/P2]
Points: [Estimate]
Status: [Draft/Refined/Ready/In Progress/Done]
```

### Story
```
As a [specific user persona],
I want to [specific action/capability],
So that [specific, measurable benefit].
```

### Context
[Background information, constraints, or assumptions]

### Acceptance Criteria
See acceptance-criteria-template.md for formats.

```
GIVEN [precondition]
WHEN [action]
THEN [expected result]
```

### Definition of Done
- [ ] Acceptance criteria met
- [ ] Code reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Accessibility requirements met
- [ ] Performance benchmarks met
- [ ] Security review complete (if applicable)
- [ ] Product owner accepted

### UX/Design
- Wireframes: [Link]
- Mockups: [Link]
- Interaction specs: [Link]

### Technical Notes
- Implementation approach: [Notes]
- APIs: [Affected endpoints]
- Database: [Schema changes]
- Dependencies: [External systems]

### Test Scenarios
| Scenario | Given | When | Then |
|----------|-------|------|------|
| Happy path | [Context] | [Action] | [Result] |
| Edge case | [Context] | [Action] | [Result] |
| Error case | [Context] | [Action] | [Error handling] |

### Open Questions
| Question | Owner | Status |
|----------|-------|--------|
| [Question] | [Who] | [Open/Resolved] |

---

## Story Splitting Patterns

### By Workflow Step
```
Original: "User can complete checkout"
Split:
- User can add items to cart
- User can enter shipping address
- User can select shipping method
- User can enter payment details
- User can confirm and place order
```

### By User Type
```
Original: "Users can manage their profile"
Split:
- Basic user can update display name
- Premium user can upload custom avatar
- Admin can edit any user's profile
```

### By Data Variation
```
Original: "Import contacts from external sources"
Split:
- Import contacts from CSV
- Import contacts from Google
- Import contacts from Outlook
```

### By Operation (CRUD)
```
Original: "Manage saved searches"
Split:
- User can create a saved search
- User can view saved searches
- User can edit a saved search
- User can delete a saved search
```

### By Platform
```
Original: "View dashboard on all devices"
Split:
- View dashboard on desktop
- View dashboard on tablet
- View dashboard on mobile
```

### By Performance
```
Original: "Search returns results"
Split:
- Search returns first 10 results immediately
- Search supports pagination for additional results
- Search caches recent queries for faster repeat searches
```

---

## Story Quality Checklist (INVEST)

- [ ] **Independent**: Can be developed without depending on other stories
- [ ] **Negotiable**: Details can be discussed, not a contract
- [ ] **Valuable**: Delivers value to user or business
- [ ] **Estimable**: Team can estimate effort
- [ ] **Small**: Can complete in one sprint
- [ ] **Testable**: Clear criteria to verify completion

---

## Story Writing Tips

### DO
- Write from user's perspective
- Include the "so that" clause (explains value)
- Keep stories small and focused
- Use concrete, specific language
- Include acceptance criteria

### DON'T
- Include technical implementation details in the story
- Write stories too large to complete in a sprint
- Use vague language ("improve," "enhance," "better")
- Skip the "so that" clause
- Combine multiple features in one story
