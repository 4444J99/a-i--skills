# /speckit.specify Command

Creates a feature specification from a natural language description.

## Usage

```
/speckit.specify <feature-description>
```

**Example**: `/speckit.specify Real-time chat system with message history and user presence`

## User Input

The text after `/speckit.specify` is the feature description. Do not ask the user to repeat it unless empty.

## Execution Workflow

### 1. Setup Feature Directory

Create the feature directory structure:
```
specs/{feature-name}/
├── spec.md
└── checklists/
    └── requirements.md
```

- Determine feature name from description (kebab-case, descriptive)
- Number features sequentially if other specs exist (001, 002, 003)
- Create branch name: `{number}-{feature-name}` (optional, suggest to user)

### 2. Load Template

Read the spec template from `assets/templates/spec-template.md` to understand required sections.

### 3. Generate Specification

Follow this workflow:

1. **Parse description**: Extract key concepts (actors, actions, data, constraints)
2. **Handle ambiguities**:
   - Make informed guesses based on context and industry standards
   - Only use `[NEEDS CLARIFICATION: question]` if:
     - Choice significantly impacts scope or UX
     - Multiple reasonable interpretations exist
     - No reasonable default exists
   - **Maximum 3 clarification markers**
   - Priority: scope > security > UX > technical
3. **Fill User Scenarios**: Prioritized user stories (P1, P2, P3)
   - Each story must be independently testable
   - Include acceptance scenarios (Given/When/Then)
4. **Generate Functional Requirements**: FR-001, FR-002, etc.
   - Each must be testable
5. **Define Success Criteria**: Measurable, technology-agnostic outcomes
6. **Identify Key Entities** (if data involved)

### 4. Write Specification

Write to `specs/{feature-name}/spec.md` using template structure.

### 5. Validate Quality

Create checklist at `specs/{feature-name}/checklists/requirements.md`:

```markdown
# Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate specification completeness before planning
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic
- [ ] All acceptance scenarios defined
- [ ] Edge cases identified
- [ ] Scope clearly bounded

## Feature Readiness

- [ ] All functional requirements have acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] No implementation details leak into specification
```

**Validation Process**:
1. Review spec against each item
2. If items fail (except clarifications): fix and re-validate (max 3 iterations)
3. If clarifications remain: present to user with options table

### 6. Handle Clarifications

If `[NEEDS CLARIFICATION]` markers remain, present to user:

```markdown
## Question 1: [Topic]

**Context**: [Quote relevant spec section]

**What we need to know**: [Specific question]

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A | [First answer] | [What this means] |
| B | [Second answer] | [What this means] |
| C | [Third answer] | [What this means] |
| Custom | Provide your own | [How to provide] |
```

Wait for user response, then update spec accordingly.

### 7. Report Completion

Report:
- Feature directory path
- Spec file path
- Checklist results
- Next step: `/speckit.plan` or `/speckit.clarify`

## Guidelines

### Focus Areas
- **WHAT** users need and **WHY**
- Avoid **HOW** (no tech stack, APIs, code structure)
- Written for business stakeholders, not developers

### Reasonable Defaults (don't ask about these)
- Data retention: Industry standard for domain
- Performance: Standard web/mobile expectations
- Error handling: User-friendly messages
- Authentication: Session-based or OAuth2 for web
- Integration: RESTful APIs

### Success Criteria Requirements
- Measurable (specific metrics)
- Technology-agnostic
- User/business focused
- Verifiable without implementation details

**Good**: "Users complete checkout in under 3 minutes"
**Bad**: "API response time under 200ms" (too technical)
