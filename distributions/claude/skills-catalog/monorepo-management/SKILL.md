---
name: monorepo-management
description: Manage monorepos and multi-package repositories with workspace tools, dependency management, selective builds, and change detection. Covers npm/pnpm workspaces, Turborepo, and Python monorepo patterns. Triggers on monorepo setup, workspace management, or multi-package repository requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - monorepo
  - workspaces
  - turborepo
  - multi-package
  - build-system
governance_phases: [shape, build]
organ_affinity: [organ-ii, organ-iii]
triggers: [user-asks-about-monorepo, context:workspace-management, project-has-turbo-json, project-has-pnpm-workspace]
complements: [python-packaging-patterns, deployment-cicd, coding-standards-enforcer]
---

# Monorepo Management

Organize and build multi-package repositories efficiently.

## When to Monorepo

| Situation | Monorepo | Polyrepo |
|-----------|----------|----------|
| Shared libraries across packages | Yes | No |
| Tight coupling between packages | Yes | No |
| Independent release cycles needed | No | Yes |
| Different teams, different cadences | No | Yes |
| Atomic cross-package changes | Yes | No |
| < 20 packages | Yes | Either |
| > 100 packages | Depends | Often better |

## JavaScript/TypeScript Workspaces

### pnpm Workspaces

```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
  - "apps/*"
  - "tools/*"
```

```json
// package.json (root)
{
  "private": true,
  "scripts": {
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint"
  }
}
```

### Package Structure

```
monorepo/
├── pnpm-workspace.yaml
├── turbo.json
├── package.json
├── packages/
│   ├── ui/                # Shared UI components
│   │   ├── package.json
│   │   └── src/
│   ├── config/            # Shared config (ESLint, TS)
│   │   └── package.json
│   └── utils/             # Shared utilities
│       └── package.json
├── apps/
│   ├── web/               # Next.js app
│   │   └── package.json
│   └── api/               # Express API
│       └── package.json
└── tools/
    └── scripts/           # Build/deploy scripts
```

### Internal Package References

```json
// apps/web/package.json
{
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "@myorg/utils": "workspace:*"
  }
}
```

## Turborepo Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "persistent": true,
      "cache": false
    }
  }
}
```

### Filtered Builds

```bash
# Build only packages affected by changes
turbo build --filter=...[HEAD~1]

# Build a specific package and its dependencies
turbo build --filter=@myorg/web

# Build everything that depends on a package
turbo build --filter=...@myorg/ui
```

## Python Monorepo Patterns

### Using a Shared Virtualenv

```
monorepo/
├── pyproject.toml          # Root with all optional deps
├── packages/
│   ├── core/
│   │   ├── pyproject.toml
│   │   └── src/core/
│   ├── api/
│   │   ├── pyproject.toml
│   │   └── src/api/
│   └── worker/
│       ├── pyproject.toml
│       └── src/worker/
└── tests/
```

```toml
# Root pyproject.toml
[project]
name = "monorepo"
dependencies = []

[project.optional-dependencies]
core = ["./packages/core"]
api = ["./packages/api"]
worker = ["./packages/worker"]
dev = ["pytest", "ruff", "mypy"]
all = ["monorepo[core,api,worker,dev]"]
```

```bash
pip install -e ".[all]"
```

### Namespace Packages

```
packages/core/src/myorg/core/__init__.py
packages/api/src/myorg/api/__init__.py
# Both install into the `myorg` namespace
```

## Dependency Management

### Version Consistency

```json
// .syncpackrc (syncpack)
{
  "versionGroups": [
    {
      "dependencies": ["react", "react-dom"],
      "packages": ["**"],
      "pinVersion": "^18.3.0"
    }
  ]
}
```

```bash
# Check version consistency
syncpack list-mismatches
# Fix mismatches
syncpack fix-mismatches
```

### Dependency Graph

```bash
# Visualize internal dependencies
turbo ls --graph

# nx
nx graph
```

## CI/CD for Monorepos

### Change Detection

```bash
#!/usr/bin/env bash
set -euo pipefail

# Detect which packages changed
CHANGED=$(git diff --name-only HEAD~1 | grep '^packages/' | cut -d/ -f2 | sort -u)

for pkg in $CHANGED; do
    echo "Building packages/$pkg"
    cd "packages/$pkg" && npm run build && cd ../..
done
```

### GitHub Actions Matrix

```yaml
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.changes.outputs.packages }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 2 }
      - id: changes
        run: |
          PKGS=$(git diff --name-only HEAD~1 | grep '^packages/' | cut -d/ -f2 | sort -u | jq -R -s -c 'split("\n") | map(select(. != ""))')
          echo "packages=$PKGS" >> $GITHUB_OUTPUT

  build:
    needs: detect-changes
    if: needs.detect-changes.outputs.packages != '[]'
    strategy:
      matrix:
        package: ${{ fromJson(needs.detect-changes.outputs.packages) }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd packages/${{ matrix.package }} && npm ci && npm run build
```

## Anti-Patterns

- **No task runner** — Manual build ordering doesn't scale; use Turborepo or Nx
- **Circular dependencies** — Packages must form a DAG; validate in CI
- **Everything in one package.json** — Separate packages even in a monorepo
- **No change detection in CI** — Building everything on every commit wastes time
- **Version drift** — Enforce consistent dependency versions with syncpack or similar
- **Implicit dependencies** — Always declare package-level dependencies explicitly
