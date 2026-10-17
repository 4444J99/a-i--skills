---
name: repo-onboarding-flow
description: Onboard new repositories into a managed ecosystem with seed.yaml contracts, CI/CD setup, documentation standards, and governance integration. Covers the full lifecycle from repo creation through promotion readiness. Triggers on new repository setup, repo onboarding, or ecosystem integration requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - onboarding
  - repository
  - governance
  - ci-cd
  - ecosystem
governance_phases: [shape]
governance_norm_group: repo-hygiene
organ_affinity: [all]
triggers: [user-asks-about-repo-onboarding, context:new-repository, context:repo-setup, context:ecosystem-integration]
complements: [python-packaging-patterns, docker-containerization, stranger-test-protocol, github-repository-standards, coding-standards-enforcer]
---

# Repository Onboarding Flow

Bring new repositories into a managed ecosystem with consistent structure and governance.

## Onboarding Checklist

```
Phase 1: Scaffold ──→ Phase 2: Configure ──→ Phase 3: Document ──→ Phase 4: Integrate ──→ Phase 5: Validate
    │                      │                      │                      │                      │
    ├─ Create repo         ├─ seed.yaml           ├─ README.md           ├─ Register in system   ├─ Stranger test
    ├─ Set structure        ├─ CI/CD               ├─ CLAUDE.md           ├─ Add to registry      ├─ CI passes
    └─ License              ├─ Linting             ├─ CONTRIBUTING.md     ├─ Wire dependencies    └─ Promotion ready
                            └─ Testing             └─ Architecture docs   └─ Event subscriptions
```

## Phase 1: Scaffold

### Repository Structure

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${1:?Usage: scaffold.sh <repo-name>}"
ORGAN="${2:?Usage: scaffold.sh <repo-name> <organ>}"

mkdir -p "${REPO_NAME}"
cd "${REPO_NAME}"
git init

# Core files
touch README.md LICENSE .gitignore

# Standard directories
mkdir -p src tests docs .github/workflows

# Python project defaults
cat > pyproject.toml << 'PYPROJECT'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "${REPO_NAME}"
version = "0.1.0"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.5"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
PYPROJECT

echo "Repository scaffolded: ${REPO_NAME}"
```

### .gitignore

```gitignore
# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
build/

# Environment
.env
.env.local
*.secret

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Build artifacts
.build/
```

## Phase 2: Configure

### seed.yaml Contract

```yaml
schema_version: "1.0"
repo: my-new-repo
organ: IV
tier: standard
promotion_status: LOCAL

produces:
  - event: repo.created
    schema: v1

consumes:
  - from: orchestration-start-here
    event: governance.updated

ci:
  - name: lint-test
    trigger: push
    agent: github-actions
```

### CI/CD Setup

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  lint-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest tests/ -v
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: detect-private-key
```

## Phase 3: Document

### README Template

```markdown
# {Repo Name}

{One-sentence description of what this does and why it exists.}

## Quick Start

### Prerequisites
- Python 3.11+
- {other prerequisites}

### Installation
\`\`\`bash
git clone {url}
cd {repo}
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
\`\`\`

### Usage
\`\`\`bash
{first command to run}
\`\`\`

## Architecture

{Brief description or diagram of how it works.}

## Development

\`\`\`bash
pytest tests/ -v          # Run tests
ruff check .              # Lint
\`\`\`

## System Context

**Organ:** {organ} | **Tier:** {tier} | **Status:** {status}
```

### CLAUDE.md

```markdown
# CLAUDE.md

## Repository Overview
{What this repo does, in context of the larger system.}

## Development Commands
\`\`\`bash
{specific commands for this repo}
\`\`\`

## Architecture
{Key patterns and decisions.}

## Key Constraints
{Things Claude needs to know to work safely in this repo.}
```

## Phase 4: Integrate

### Register in System

```python
def register_repo(registry_path: str, repo: dict):
    registry = json.loads(Path(registry_path).read_text())
    # Validate minimum fields
    assert repo["name"], "Name required"
    assert repo["organ"] in VALID_ORGANS, f"Invalid organ: {repo['organ']}"
    assert repo["tier"] in VALID_TIERS, f"Invalid tier: {repo['tier']}"

    registry["repos"].append(repo)
    Path(registry_path).write_text(json.dumps(registry, indent=2))
```

### Dependency Wiring

```yaml
# In seed.yaml, declare edges
consumes:
  - from: orchestration-start-here
    event: governance.updated
  - from: meta/organvm-engine
    event: registry.refreshed

produces:
  - event: my-repo.deployed
    schema: v1
```

## Phase 5: Validate

### Onboarding Validation Checklist

```python
def validate_onboarding(repo_path: str) -> list[str]:
    issues = []
    p = Path(repo_path)

    # Core files
    for f in ["README.md", "LICENSE", ".gitignore", "seed.yaml"]:
        if not (p / f).exists():
            issues.append(f"Missing: {f}")

    # seed.yaml valid
    if (p / "seed.yaml").exists():
        seed = yaml.safe_load((p / "seed.yaml").read_text())
        for field in ["schema_version", "repo", "organ", "tier", "promotion_status"]:
            if field not in seed:
                issues.append(f"seed.yaml missing: {field}")

    # CI exists
    if not list((p / ".github/workflows").glob("*.yml")):
        issues.append("No CI workflow found")

    # README quality
    readme = (p / "README.md").read_text() if (p / "README.md").exists() else ""
    if len(readme.split()) < 50:
        issues.append("README too short (< 50 words)")

    return issues
```

### Stranger Test Integration

After onboarding, run the stranger-test-protocol against the README and documentation to verify a newcomer can understand the repository.

## Promotion Readiness

| Status | Requirements |
|--------|-------------|
| **LOCAL** | seed.yaml + README + .gitignore |
| **CANDIDATE** | + CI passing + tests + CLAUDE.md |
| **PUBLIC_PROCESS** | + Stranger test passed + full docs |
| **GRADUATED** | + Production usage + monitoring |

## Anti-Patterns

- **No seed.yaml** — Every repo needs its ecosystem contract
- **Skipping documentation** — Documentation gaps compound over time
- **Manual CI setup** — Template from existing repos; don't start from scratch
- **No validation step** — Always validate before declaring onboarding complete
- **Orphaned repos** — Register in the system registry immediately
- **Copy-paste without adaptation** — Templates are starting points; customize per repo
