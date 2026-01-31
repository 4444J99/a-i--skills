# Built-in Chains

Pre-built workflow chains for common development scenarios.

## Development Chains

### api-development

Full API lifecycle from design to deployment.

```yaml
chain:
  name: api-development
  description: Full API development from design to deployment

steps:
  - id: design
    skill: api-design-patterns
    description: Design API structure and contracts
    outputs: [openapi-spec, endpoint-list, data-models]

  - id: test-first
    skill: tdd-workflow
    description: Write tests before implementation
    depends_on: [design]
    outputs: [test-suite]

  - id: implement
    skill: backend-implementation-patterns
    description: Implement API endpoints
    depends_on: [test-first]
    outputs: [source-code]

  - id: verify
    skill: verification-loop
    description: Verify implementation meets requirements
    depends_on: [implement]
    checkpoint: true
    outputs: [verification-report]

  - id: deploy
    skill: deployment-cicd
    description: Deploy to staging/production
    depends_on: [verify]
    optional: true
```

**Use when**: Building a new API or significant API changes

**Duration**: Medium to large scope

---

### fullstack-feature

Complete feature implementation across the stack.

```yaml
chain:
  name: fullstack-feature
  description: Implement a complete full-stack feature

steps:
  - id: requirements
    skill: product-requirements-designer
    description: Define feature requirements and acceptance criteria
    outputs: [prd, user-stories, acceptance-criteria]

  - id: api
    skill: api-design-patterns
    description: Design API contract for the feature
    depends_on: [requirements]
    outputs: [openapi-spec, endpoints]

  - id: backend
    skill: backend-implementation-patterns
    description: Implement backend services
    depends_on: [api]
    outputs: [backend-code]

  - id: frontend
    skill: frontend-design-systems
    description: Build frontend components
    depends_on: [api]
    outputs: [components, pages]

  - id: testing
    skill: testing-patterns
    description: Write comprehensive tests
    depends_on: [backend, frontend]
    outputs: [test-suite]

  - id: verify
    skill: verification-loop
    description: End-to-end verification
    depends_on: [testing]
    checkpoint: true
```

**Use when**: Adding a new feature that spans frontend and backend

**Duration**: Large scope

---

### mcp-development

Create an MCP (Model Context Protocol) server.

```yaml
chain:
  name: mcp-development
  description: Build an MCP server from concept to deployment

steps:
  - id: design
    skill: mcp-builder
    description: Design and scaffold MCP server
    outputs: [mcp-server, tools-list, schema]

  - id: test
    skill: testing-patterns
    description: Write tests for MCP tools
    depends_on: [design]
    outputs: [test-suite]

  - id: verify
    skill: verification-loop
    description: Verify MCP server functionality
    depends_on: [test]
    checkpoint: true
    outputs: [verification-report]

  - id: orchestrate
    skill: mcp-server-orchestrator
    description: Configure server orchestration
    depends_on: [verify]
    optional: true
```

**Use when**: Building a new MCP server

**Duration**: Medium scope

---

## Professional Chains

### career-preparation

Prepare for job search and interviews.

```yaml
chain:
  name: career-preparation
  description: Complete job search preparation workflow

steps:
  - id: resume
    skill: cv-resume-builder
    description: Create or update resume/CV
    outputs: [resume, skills-summary]

  - id: portfolio
    skill: portfolio-presentation
    description: Build portfolio presentation
    depends_on: [resume]
    outputs: [portfolio, case-studies]

  - id: interview
    skill: interview-preparation
    description: Prepare for interviews
    depends_on: [portfolio]
    outputs: [interview-prep, talking-points]
    checkpoint: true

  - id: networking
    skill: networking-outreach
    description: Create networking strategy
    depends_on: [resume]
    optional: true
    outputs: [outreach-templates, contact-list]
```

**Use when**: Preparing for job search or career transition

**Duration**: Medium scope

---

### documentation

Create comprehensive project documentation.

```yaml
chain:
  name: documentation
  description: Generate complete project documentation

steps:
  - id: docs
    skill: doc-coauthoring
    description: Write project documentation
    outputs: [readme, guides, api-docs]

  - id: repo-standards
    skill: github-repository-standards
    description: Set up repository standards
    depends_on: [docs]
    outputs: [contributing, issue-templates, pr-templates]

  - id: profile
    skill: github-profile-architect
    description: Update GitHub profile
    depends_on: [docs]
    optional: true
```

**Use when**: Setting up or improving project documentation

**Duration**: Small to medium scope

---

## Quick Reference

| Chain | Steps | Primary Skills | Scope |
|-------|-------|----------------|-------|
| api-development | 5 | api-design-patterns, backend-implementation-patterns | Medium |
| fullstack-feature | 6 | Multiple frontend + backend | Large |
| mcp-development | 4 | mcp-builder, testing-patterns | Medium |
| career-preparation | 4 | cv-resume-builder, interview-preparation | Medium |
| documentation | 3 | doc-coauthoring, github-repository-standards | Small |

## Chain Selection Guide

**Building an API?**
→ Use `api-development`

**Adding a new feature?**
→ Use `fullstack-feature`

**Creating an MCP server?**
→ Use `mcp-development`

**Job hunting?**
→ Use `career-preparation`

**Setting up docs?**
→ Use `documentation`

**Custom workflow?**
→ Start with `custom-chain.yaml` template

## Customization

All chains can be customized:

1. Copy chain YAML to your project
2. Modify steps as needed:
   - Add/remove steps
   - Change dependencies
   - Adjust checkpoints
   - Mark steps optional
3. Run with `/skill-chain-prompts run` and paste your chain

Or describe your needs and Claude will generate a custom chain.
