---
name: python-packaging-patterns
description: Structure Python projects for distribution with pyproject.toml, src layouts, dependency management, and publishing workflows. Covers packaging tools (hatch, setuptools, flit, poetry), versioning strategies, and editable installs. Triggers on Python project setup, packaging configuration, or dependency management requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - python
  - packaging
  - pyproject
  - dependencies
  - distribution
governance_phases: [shape, build]
governance_norm_group: repo-hygiene
organ_affinity: [organ-i, organ-iv, organ-v, organ-vi, organ-vii, meta]
triggers: [user-asks-about-python-packaging, project-has-pyproject-toml, project-has-setup-py, context:new-python-project, file-type:pyproject.toml]
complements: [deployment-cicd, testing-patterns, coding-standards-enforcer]
---

# Python Packaging Patterns

Structure Python projects for reliable distribution and dependency management.

## Project Layout

### The `src` Layout (Recommended)

```
my-project/
├── pyproject.toml
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── conftest.py
│   └── test_core.py
└── README.md
```

**Why src layout:** Prevents accidental imports from the working directory. Forces installation before testing, catching packaging errors early.

### Flat Layout (Simple Projects)

```
my-project/
├── pyproject.toml
├── my_package/
│   ├── __init__.py
│   └── core.py
└── tests/
```

Acceptable for internal tools and single-organ repos where distribution is not a concern.

## pyproject.toml Configuration

### Minimal Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "A concise description"
requires-python = ">=3.11"
license = "MIT"
dependencies = [
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.5",
    "mypy>=1.10",
]
```

### Build Backend Selection

| Backend | When to Use |
|---------|-------------|
| **hatchling** | Default choice. Fast, minimal config, good monorepo support |
| **setuptools** | Legacy projects, C extensions, complex build needs |
| **flit** | Pure Python, minimal config, simple projects |
| **poetry-core** | When using Poetry for dependency management |

### Optional Dependency Groups

Organize optional dependencies by use case:

```toml
[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.5", "mypy>=1.10"]
docs = ["sphinx>=7.0", "myst-parser"]
dashboard = ["fastapi>=0.110", "uvicorn"]
metrics = ["prometheus-client"]
```

Install specific groups: `pip install -e ".[dev,dashboard]"`

## Entry Points

### Console Scripts

```toml
[project.scripts]
my-cli = "my_package.cli:main"
```

### Plugin Entry Points

```toml
[project.entry-points."my_app.plugins"]
csv = "my_package.plugins.csv:CsvPlugin"
json = "my_package.plugins.json:JsonPlugin"
```

## Version Management

### Single Source of Truth

```toml
# In pyproject.toml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "src/my_package/__init__.py"
```

```python
# In __init__.py
__version__ = "0.1.0"
```

### CalVer for System Packages

For infrastructure packages where semantic versioning adds little value:

```python
__version__ = "2026.03.1"  # YYYY.MM.patch
```

## Dependency Pinning Strategy

| Context | Strategy | Tool |
|---------|----------|------|
| Library | Loose bounds (`>=1.0,<2.0`) | pyproject.toml |
| Application | Exact pins | pip-compile / uv lock |
| CI | Lockfile | uv.lock / requirements.txt |

### Generating Lockfiles

```bash
# Using uv (recommended)
uv pip compile pyproject.toml -o requirements.txt
uv pip compile pyproject.toml --extra dev -o requirements-dev.txt

# Using pip-tools
pip-compile pyproject.toml -o requirements.txt
```

## Editable Installs

```bash
# Standard editable install
pip install -e .

# With dev dependencies
pip install -e ".[dev]"

# In a fresh venv
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Tool Configuration in pyproject.toml

### Ruff

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

### Pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
pythonpath = ["."]
```

### Mypy

```toml
[tool.mypy]
strict = true
python_version = "3.11"
```

## Publishing

### To PyPI

```bash
# Build
python -m build

# Upload (use trusted publishing when possible)
python -m twine upload dist/*
```

### Trusted Publishing (GitHub Actions)

```yaml
- uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
```

## Common Patterns

### Namespace Packages

For multi-repo packages sharing a namespace:

```
# Repo A
src/organvm/engine/__init__.py

# Repo B
src/organvm/dashboard/__init__.py
```

Use implicit namespace packages (no `__init__.py` at namespace level).

### Conditional Dependencies

```toml
dependencies = [
    "tomli>=2.0; python_version < '3.11'",
    "typing-extensions>=4.0; python_version < '3.12'",
]
```

### Package Data

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

[tool.hatch.build.targets.wheel.force-include]
"assets" = "my_package/assets"
```

## Anti-Patterns to Avoid

- **setup.py without pyproject.toml** — Always use pyproject.toml as the single config source
- **Pinning exact versions in libraries** — Use compatible ranges to avoid dependency conflicts
- **Importing from project root in tests** — Use src layout or ensure editable install
- **Multiple version sources** — Keep version in exactly one place
- **requirements.txt as sole dependency spec** — Use pyproject.toml; generate lockfiles from it
