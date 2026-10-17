# GitHub Actions CI/CD Workflows

Common workflow patterns for automating builds, tests, and deployments.

---

## Workflow Basics

GitHub Actions workflows live in `.github/workflows/` as YAML files. They run on events like pushes, pull requests, and schedules.

### Minimal Workflow Structure

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

Key concepts:
- **Triggers** (`on`): Events that start the workflow
- **Jobs**: Groups of steps that run on a fresh VM
- **Steps**: Individual commands or actions
- **Actions**: Reusable units from the marketplace (e.g., `actions/checkout@v4`)

---

## Common Triggers

| Trigger | Use Case |
|---------|----------|
| `push` | Run on every push to specified branches |
| `pull_request` | Run checks on PRs before merge |
| `schedule` (cron) | Nightly builds, dependency audits |
| `release` | Publish packages on new release |
| `workflow_dispatch` | Manual trigger with optional inputs |

### Branch and Path Filtering

```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - '**.md'
```

---

## CI Workflow Example (Node.js)

```yaml
name: Node.js CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

Adapt for other languages by swapping `setup-node` for `setup-python`, `setup-go`, etc.

---

## Reusable Patterns

### Job Dependencies

Use `needs` to create sequential pipelines:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint
  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
  deploy:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

### Secrets

Never hardcode secrets. Store them in Settings > Secrets and variables, then reference with `${{ secrets.MY_SECRET }}`.

---

## Release and Publish

### npm Package Publishing

```yaml
name: Publish
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # allow-secret
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### GitHub Pages Deployment

Use `actions/upload-pages-artifact` and `actions/deploy-pages` to deploy a static build directory. Set `permissions` for `pages: write` and `id-token: write`. <!-- allow-secret -->

---

## Quality Gates

Require workflows to pass before merging via Settings > Branches > Branch protection rules. Add coverage with `codecov/codecov-action` and security scanning with `github/codeql-action/analyze`.

---

## Workflow Tips

| Tip | Why |
|-----|-----|
| Pin action versions with SHA | Prevents supply chain attacks |
| Use `concurrency` to cancel stale runs | Saves minutes on rapid pushes |
| Keep workflows under 10 minutes | Faster feedback, lower costs |
| Split lint/test/build into separate jobs | Parallel execution, clearer failures |
| Use `paths` filters | Skip runs when only docs change |

### Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## Starter Workflow Checklist

For a new repository, set up these workflows in order:

1. **CI** -- lint + test on PRs and pushes to main
2. **Security** -- CodeQL or Dependabot alerts
3. **Release** -- publish on tag or GitHub release
4. **Deploy** -- Pages, cloud provider, or container registry
