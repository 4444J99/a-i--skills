# Development Patterns Ecosystem

This guide maps the relationships between development-focused skills in this repository and provides workflow guidance for using them together effectively.

## Skill Overview

| Skill | Category | Focus Area |
|-------|----------|------------|
| [`api-design-patterns`](../../skills/development/api-design-patterns/) | development | REST, GraphQL, versioning |
| [`backend-implementation-patterns`](../../skills/development/backend-implementation-patterns/) | development | API implementation, auth, validation |
| [`testing-patterns`](../../skills/development/testing-patterns/) | development | Unit, integration, E2E testing |
| [`tdd-workflow`](../../skills/development/tdd-workflow/) | development | Test-driven development process |
| [`verification-loop`](../../skills/development/verification-loop/) | development | Pre-commit quality verification |
| [`code-refactoring-patterns`](../../skills/development/code-refactoring-patterns/) | development | Refactoring techniques |
| [`deployment-cicd`](../../skills/development/deployment-cicd/) | development | CI/CD pipelines |
| [`mcp-builder`](../../skills/development/mcp-builder/) | development | MCP server development |
| [`mcp-server-orchestrator`](../../skills/development/mcp-server-orchestrator/) | development | Multi-server coordination |
| [`frontend-design-systems`](../../skills/development/frontend-design-systems/) | development | Component libraries |
| [`responsive-design-patterns`](../../skills/development/responsive-design-patterns/) | development | Mobile-first design |
| [`nextjs-fullstack-patterns`](../../skills/development/nextjs-fullstack-patterns/) | development | Next.js App Router |
| [`postgres-advanced-patterns`](../../skills/development/postgres-advanced-patterns/) | development | Database optimization |
| [`rust-systems-design`](../../skills/development/rust-systems-design/) | development | Rust architecture |
| [`accessibility-patterns`](../../skills/development/accessibility-patterns/) | development | WCAG compliance |

## Ecosystem Diagram

```mermaid
flowchart TB
    subgraph Design["API & Architecture"]
        API[api-design-patterns]
        MCP[mcp-builder]
    end

    subgraph Implementation["Implementation"]
        BE[backend-implementation-patterns]
        FE[frontend-design-systems]
        NJS[nextjs-fullstack-patterns]
        PG[postgres-advanced-patterns]
    end

    subgraph Quality["Quality Assurance"]
        TEST[testing-patterns]
        TDD[tdd-workflow]
        VER[verification-loop]
        REF[code-refactoring-patterns]
    end

    subgraph Deploy["Deployment"]
        CICD[deployment-cicd]
        MCPO[mcp-server-orchestrator]
    end

    API -->|"Implement"| BE
    API -->|"Alternative"| MCP
    BE -->|"Test with"| TEST
    MCP -->|"Test with"| TEST
    TEST -->|"Use in"| TDD
    TDD -->|"Verify via"| VER
    VER -->|"Before"| CICD
    FE -->|"Test with"| TEST
    NJS -->|"Uses"| BE
    NJS -->|"Uses"| FE
    BE -->|"Connects to"| PG
    MCP -->|"Orchestrate"| MCPO
    REF -.->|"Improve"| BE
    REF -.->|"Improve"| FE

    style API fill:#e3f2fd
    style BE fill:#e8f5e9
    style TEST fill:#fff3e0
    style CICD fill:#f3e5f5
```

## Workflow Scenarios

### Scenario 1: New API Development

**Goal:** Build a production-ready REST API from design to deployment.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant API as api-design-patterns
    participant BE as backend-implementation
    participant TDD as tdd-workflow
    participant VER as verification-loop
    participant CICD as deployment-cicd

    Dev->>API: 1. Design API structure
    API-->>Dev: OpenAPI spec, endpoints
    Dev->>TDD: 2. Write failing tests
    TDD-->>Dev: Test stubs
    Dev->>BE: 3. Implement endpoints
    BE-->>Dev: Working API
    Dev->>VER: 4. Run verification
    VER-->>Dev: Build, lint, test pass
    Dev->>CICD: 5. Deploy
    CICD-->>Dev: Production deployment
```

**Skill Sequence:**
1. **`api-design-patterns`** - Design endpoints, response formats, error handling
2. **`tdd-workflow`** - Write tests for each endpoint
3. **`backend-implementation-patterns`** - Implement API logic
4. **`verification-loop`** - Ensure all quality gates pass
5. **`deployment-cicd`** - Set up CI pipeline and deploy

### Scenario 2: MCP Server Development

**Goal:** Create an MCP server that integrates with external services.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant MCP as mcp-builder
    participant TEST as testing-patterns
    participant VER as verification-loop
    participant MCPO as mcp-server-orchestrator

    Dev->>MCP: 1. Research API, plan tools
    MCP-->>Dev: Tool designs
    Dev->>MCP: 2. Implement server
    MCP-->>Dev: Working MCP server
    Dev->>TEST: 3. Create evaluations
    TEST-->>Dev: Evaluation suite
    Dev->>VER: 4. Verify quality
    VER-->>Dev: All checks pass
    Dev->>MCPO: 5. Add to orchestration (optional)
    MCPO-->>Dev: Multi-server setup
```

**Skill Sequence:**
1. **`mcp-builder`** - Deep research, plan tools, implement server
2. **`testing-patterns`** - Create evaluation questions
3. **`verification-loop`** - Run quality checks
4. **`mcp-server-orchestrator`** - Coordinate with other servers (if needed)

### Scenario 3: Full-Stack Feature Development

**Goal:** Add a feature spanning frontend, backend, and database.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant API as api-design-patterns
    participant PG as postgres-patterns
    participant BE as backend-implementation
    participant FE as frontend-design-systems
    participant TDD as tdd-workflow
    participant VER as verification-loop

    Dev->>API: 1. Design feature API
    API-->>Dev: Endpoint specs
    Dev->>PG: 2. Design data model
    PG-->>Dev: Schema, queries
    Dev->>TDD: 3. Write tests
    TDD-->>Dev: Test suite
    Dev->>BE: 4. Implement backend
    BE-->>Dev: API endpoints
    Dev->>FE: 5. Implement frontend
    FE-->>Dev: UI components
    Dev->>VER: 6. Verify all layers
    VER-->>Dev: Integration pass
```

**Skill Sequence:**
1. **`api-design-patterns`** - Design feature endpoints
2. **`postgres-advanced-patterns`** - Data modeling, queries
3. **`tdd-workflow`** - Test-first approach
4. **`backend-implementation-patterns`** - Backend logic
5. **`frontend-design-systems`** - UI components
6. **`verification-loop`** - End-to-end verification

## Decision Tree: Which Development Skill?

```mermaid
flowchart TD
    A[What are you building?] --> B{API?}
    B -->|REST/GraphQL| API[api-design-patterns]
    B -->|MCP Server| MCP[mcp-builder]
    B -->|No| C{Frontend?}

    C -->|Yes| D{Framework?}
    D -->|Next.js| NJS[nextjs-fullstack-patterns]
    D -->|Other| FE[frontend-design-systems]

    C -->|No| E{Database?}
    E -->|PostgreSQL| PG[postgres-advanced-patterns]
    E -->|No| F{Quality?}

    F -->|Testing| TEST[testing-patterns]
    F -->|TDD| TDD[tdd-workflow]
    F -->|Verification| VER[verification-loop]
    F -->|Refactoring| REF[code-refactoring-patterns]

    API --> BE[backend-implementation-patterns]
    MCP --> TEST
```

## Cross-Reference Matrix

| When using... | Consider also... | Reason |
|---------------|------------------|--------|
| api-design-patterns | backend-implementation-patterns | Design then implement |
| backend-implementation-patterns | postgres-advanced-patterns | Data layer integration |
| testing-patterns | tdd-workflow | TDD uses testing patterns |
| tdd-workflow | verification-loop | Verify before commit |
| mcp-builder | testing-patterns | Evaluation suite |
| frontend-design-systems | accessibility-patterns | Inclusive design |
| nextjs-fullstack-patterns | deployment-cicd | Vercel/deployment |

## Handoff Patterns

### From Design to Implementation
```
api-design-patterns → backend-implementation-patterns
├─ Pass: OpenAPI spec, endpoint list
├─ Expect: Implementation follows spec
└─ Verify: Responses match documented formats
```

### From Implementation to Testing
```
backend-implementation-patterns → testing-patterns
├─ Pass: Endpoint implementations
├─ Expect: Unit + integration tests
└─ Verify: Coverage > 80%
```

### From Testing to Deployment
```
verification-loop → deployment-cicd
├─ Pass: All checks green
├─ Expect: CI pipeline succeeds
└─ Verify: Deployed version works
```

## Integration Checklist

### Starting a New Project
- [ ] Choose API approach (REST/GraphQL vs MCP)
- [ ] Design data model with `postgres-advanced-patterns`
- [ ] Set up testing with `testing-patterns`
- [ ] Configure CI with `deployment-cicd`

### Adding a Feature
- [ ] Design endpoints with `api-design-patterns`
- [ ] Write tests first with `tdd-workflow`
- [ ] Implement with `backend-implementation-patterns`
- [ ] Verify with `verification-loop`

### Improving Code Quality
- [ ] Refactor with `code-refactoring-patterns`
- [ ] Add tests with `testing-patterns`
- [ ] Verify changes with `verification-loop`
