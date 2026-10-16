# Agent Type Catalog

Comprehensive reference for agent types, their capabilities, and appropriate use cases.

## Agent Types Overview

| Agent | Primary Function | Access Level | Best For |
|-------|------------------|--------------|----------|
| Explore | Read-only analysis | Read files, search | Research, understanding |
| Plan | Architecture design | Read + design | System design, planning |
| Bash | Command execution | Run commands | Tests, builds, git |
| Edit | File modification | Read + write | Implementation |

## Explore Agent

### Capabilities

- Read files and directories
- Search codebase with Glob/Grep
- Analyze code patterns
- Navigate documentation
- No file modifications

### Use Cases

```yaml
explore_tasks:
  - "Find all files using deprecated API"
  - "Understand authentication flow"
  - "Locate configuration files"
  - "Map module dependencies"
  - "Research existing patterns"
  - "Count usage of specific function"
```

### Task Template

```yaml
- id: E1
  name: "Research current auth implementation"
  agent: Explore
  objectives:
    - "Find auth-related files"
    - "Document current flow"
    - "Identify extension points"
  outputs:
    - research_notes.md
  estimated: 15min
```

### Best Practices

```yaml
do:
  - Use for initial codebase understanding
  - Gather context before implementation
  - Find patterns to follow
  - Identify related files

dont:
  - Use when you already know the file locations
  - Use for simple, direct queries
  - Use when modification is needed
```

## Plan Agent

### Capabilities

- All Explore capabilities
- System architecture design
- Dependency analysis
- Implementation planning
- Create design documents

### Use Cases

```yaml
plan_tasks:
  - "Design API for new feature"
  - "Architect microservice boundaries"
  - "Plan database schema changes"
  - "Create implementation roadmap"
  - "Analyze impact of changes"
  - "Design component interfaces"
```

### Task Template

```yaml
- id: P1
  name: "Design user notification system"
  agent: Plan
  inputs:
    - requirements.md
    - current_architecture.md
  objectives:
    - "Define component boundaries"
    - "Specify data flow"
    - "Document API contracts"
  outputs:
    - notification_design.md
    - api_contract.yaml
  estimated: 30min
```

### Best Practices

```yaml
do:
  - Use for non-trivial features
  - Create before implementation
  - Define clear interfaces
  - Consider edge cases

dont:
  - Over-plan simple changes
  - Skip for obvious implementations
  - Create without context gathering first
```

## Bash Agent

### Capabilities

- Execute shell commands
- Run tests
- Build projects
- Git operations
- File system commands
- Install dependencies

### Use Cases

```yaml
bash_tasks:
  - "Run test suite"
  - "Build production bundle"
  - "Execute database migrations"
  - "Commit and push changes"
  - "Install dependencies"
  - "Start/stop services"
```

### Task Template

```yaml
- id: B1
  name: "Run full test suite"
  agent: Bash
  commands:
    - "npm install"
    - "npm run test"
    - "npm run lint"
  success_criteria:
    - exit_code: 0
    - output_contains: "All tests passed"
  estimated: 5min
```

### Best Practices

```yaml
do:
  - Verify before destructive operations
  - Check exit codes
  - Capture output for analysis
  - Use for automation

dont:
  - Use for complex file editing
  - Assume commands succeed
  - Skip error handling
```

### Common Command Patterns

```bash
# Testing
npm run test
pytest tests/
go test ./...

# Building
npm run build
cargo build --release
go build .

# Git operations
git status
git add -A
git commit -m "message"
git push origin branch

# Dependencies
npm install package
pip install package
go get package
```

## Edit Agent

### Capabilities

- All Explore capabilities
- Create new files
- Modify existing files
- Refactor code
- Apply patches

### Use Cases

```yaml
edit_tasks:
  - "Implement new feature"
  - "Fix bug in module"
  - "Refactor legacy code"
  - "Add unit tests"
  - "Update configuration"
  - "Apply code review feedback"
```

### Task Template

```yaml
- id: D1
  name: "Implement user authentication"
  agent: Edit
  inputs:
    - auth_design.md
    - api_contract.yaml
  files_to_create:
    - src/auth/authenticator.py
    - src/auth/middleware.py
    - tests/auth/test_authenticator.py
  files_to_modify:
    - src/routes.py
    - src/config.py
  estimated: 45min
```

### Best Practices

```yaml
do:
  - Follow existing code patterns
  - Add tests with implementation
  - Make focused, atomic changes
  - Preserve existing formatting

dont:
  - Make unrelated changes
  - Skip testing
  - Ignore linting rules
  - Over-engineer
```

## Agent Selection Guide

### Decision Tree

```
Need to modify files?
├── Yes → Edit Agent
└── No → Need to run commands?
         ├── Yes → Bash Agent
         └── No → Need to design solution?
                  ├── Yes → Plan Agent
                  └── No → Explore Agent
```

### By Task Type

| Task Type | Primary Agent | Supporting Agents |
|-----------|---------------|-------------------|
| Research | Explore | - |
| Design | Plan | Explore |
| Implementation | Edit | Explore |
| Testing | Bash | Edit (for fixes) |
| Refactoring | Edit | Explore, Plan |
| Deployment | Bash | - |
| Bug Fix | Edit | Explore, Bash |
| Code Review | Explore | Edit (for fixes) |

### By Phase

| Development Phase | Agents Used |
|-------------------|-------------|
| Discovery | Explore |
| Architecture | Plan, Explore |
| Implementation | Edit, Bash |
| Testing | Bash, Edit |
| Integration | Edit, Bash |
| Deployment | Bash |

## Agent Communication

### Handoff Pattern

```yaml
workflow:
  - step: 1
    agent: Explore
    output: "research_findings.md"
    handoff_to: Plan

  - step: 2
    agent: Plan
    input: "research_findings.md"
    output: "implementation_plan.md"
    handoff_to: Edit

  - step: 3
    agent: Edit
    input: "implementation_plan.md"
    output: [modified_files]
    handoff_to: Bash

  - step: 4
    agent: Bash
    input: [modified_files]
    command: "npm run test"
    verify: exit_code == 0
```

### Information Passing

```yaml
artifacts:
  - name: "research_findings"
    producer: Explore
    consumers: [Plan, Edit]
    format: markdown

  - name: "api_contract"
    producer: Plan
    consumers: [Edit]
    format: yaml

  - name: "implementation"
    producer: Edit
    consumers: [Bash]
    format: source_files
```

## Performance Characteristics

| Agent | Startup Time | Typical Duration | Parallelizable |
|-------|--------------|------------------|----------------|
| Explore | Fast | 5-30 min | Yes |
| Plan | Fast | 15-60 min | Limited |
| Bash | Fast | 1-10 min | Yes* |
| Edit | Fast | 15-120 min | Yes |

*Bash agents may conflict on shared resources
