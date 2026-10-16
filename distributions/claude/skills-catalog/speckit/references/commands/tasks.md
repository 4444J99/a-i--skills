# /speckit.tasks Command

Generates an executable, dependency-ordered task list from the implementation plan.

## Usage

```
/speckit.tasks
```

## Prerequisites

Required files in feature directory:
- `plan.md` - Tech stack, structure
- `spec.md` - User stories with priorities

Optional files:
- `data-model.md` - Entities
- `contracts/` - API endpoints
- `research.md` - Technology decisions
- `quickstart.md` - Test scenarios

## Execution Workflow

### 1. Load Design Documents

Read from the feature directory:
```
specs/{feature-name}/
├── plan.md          # Required
├── spec.md          # Required
├── data-model.md    # Optional
├── contracts/       # Optional
├── research.md      # Optional
└── quickstart.md    # Optional
```

Not all projects have all documents. Generate tasks based on what's available.

### 2. Extract Information

From `plan.md`:
- Tech stack and libraries
- Project structure and paths

From `spec.md`:
- User stories with priorities (P1, P2, P3)
- Acceptance criteria

From `data-model.md` (if exists):
- Entities → model tasks

From `contracts/` (if exists):
- Endpoints → API tasks

From `research.md` (if exists):
- Decisions → setup tasks

### 3. Generate Tasks

**Task Format**: `[ID] [P?] [Story] Description`
- `[P]` = Parallelizable (different files, no dependencies)
- `[Story]` = User story label (US1, US2, US3)
- Include exact file paths

**Organization by Phase**:

#### Phase 1: Setup (Shared Infrastructure)
- Project structure creation
- Dependency installation
- Linting/formatting config

#### Phase 2: Foundational (Blocking Prerequisites)
- Database schema/migrations
- Authentication framework
- API routing/middleware
- Base models used by all stories
- Error handling infrastructure

**CRITICAL**: No user story can start until Phase 2 completes.

#### Phase 3+: User Stories (P1, P2, P3...)

Each user story gets its own phase:

```markdown
## Phase 3: User Story 1 - [Title] (Priority: P1)

**Goal**: [What this story delivers]
**Independent Test**: [How to verify it works alone]

### Tests (OPTIONAL - only if requested)
- [ ] T00X [P] [US1] Contract test for [endpoint]
- [ ] T00X [P] [US1] Integration test for [journey]

### Implementation
- [ ] T00X [P] [US1] Create [Entity] model
- [ ] T00X [US1] Implement [Service]
- [ ] T00X [US1] Implement [endpoint]

**Checkpoint**: User Story 1 fully functional
```

#### Final Phase: Polish & Cross-Cutting
- Documentation
- Code cleanup
- Performance optimization
- Security hardening

### 4. Task Generation Rules

**Tests are OPTIONAL**: Only include if explicitly requested in spec or user asks for TDD.

**From User Stories**:
- Each story gets its own phase
- Map components to their story
- Most stories should be independent

**From Contracts**:
- Map endpoints to user stories
- Contract tests before implementation (if tests requested)

**From Data Model**:
- Map entities to stories
- Shared entities → Setup or Foundational phase

**Parallelization**:
- Different files = mark `[P]`
- Same file = sequential (no `[P]`)

**Ordering within story**:
- Tests (if requested) → Models → Services → Endpoints

### 5. Generate Dependencies Section

```markdown
## Dependencies & Execution Order

### Phase Dependencies
- Setup: No dependencies
- Foundational: Depends on Setup - BLOCKS all user stories
- User Stories: All depend on Foundational completion
- Polish: Depends on desired stories complete

### User Story Dependencies
- US1 (P1): Can start after Foundational
- US2 (P2): Can start after Foundational
- US3 (P3): Can start after Foundational

### Parallel Opportunities
- All [P] tasks within a phase can run together
- Different user stories can run in parallel (if team allows)
```

### 6. Generate Implementation Strategy

```markdown
## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Setup + Foundational
2. Complete User Story 1
3. STOP and VALIDATE
4. Deploy/demo if ready

### Incremental Delivery
1. Setup + Foundational → Foundation ready
2. User Story 1 → Test → Deploy (MVP!)
3. User Story 2 → Test → Deploy
4. Continue incrementally
```

### 7. Write tasks.md

Use `assets/templates/tasks-template.md` as structure.

Output to `specs/{feature-name}/tasks.md`.

### 8. Report Summary

- Total task count
- Task count per user story
- Parallel opportunities
- Independent test criteria per story
- Suggested MVP scope

## Path Conventions

- **Single project**: `src/`, `tests/`
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`

Adjust based on structure in `plan.md`.

## Quality Criteria

Each task must be:
- Specific enough for an LLM to complete without additional context
- Include exact file paths
- Clearly labeled with story ownership
- Part of a coherent execution order
