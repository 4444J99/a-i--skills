# GitHub Actions Recipes

Common workflow patterns for CI/CD with GitHub Actions.

## Conditional Jobs

### Run only on specific paths

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
      - '.github/workflows/ci.yml'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

### Skip CI

```yaml
# Commit message contains [skip ci]
on:
  push:
    branches: [main]

jobs:
  build:
    if: "!contains(github.event.head_commit.message, '[skip ci]')"
    runs-on: ubuntu-latest
    steps: ...
```

### Branch-specific deployment

```yaml
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps: ...

  deploy-production:
    if: github.ref == 'refs/heads/main'
    environment: production
    steps: ...
```

## Reusable Workflows

### Define a reusable workflow

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
    secrets:
      DATABASE_URL:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Call the reusable workflow

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
    secrets:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Database Service Containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
```

## Artifact Management

### Upload build output

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-${{ github.sha }}
    path: dist/
    retention-days: 7
```

### Download in a later job

```yaml
deploy:
  needs: build
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: build-${{ github.sha }}
        path: dist/
```

## PR Comments and Annotations

### Post a comment on PR

```yaml
- uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '## Build Report\n\nBundle size: 142kb (gzipped)'
      })
```

### Annotate files with warnings

```yaml
- run: |
    echo "::warning file=src/api.ts,line=42::Deprecated function used"
    echo "::error file=src/config.ts,line=10::Missing required field"
```

## Scheduled Workflows

```yaml
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 6am UTC

jobs:
  dependency-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --production
      - run: npx license-checker --failOn 'GPL-3.0'
```

## Concurrency Control

```yaml
# Cancel in-progress runs for the same branch
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Environment Protection Rules

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - run: echo "Deploying to production"
```

Configure in GitHub: Settings > Environments > production > Add required reviewers.

## Composite Actions

### Create a local composite action

```yaml
# .github/actions/setup-project/action.yml
name: Setup Project
description: Install Node.js and dependencies

inputs:
  node-version:
    description: Node.js version
    default: '20'

runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    - run: npm ci
      shell: bash
```

### Use it in workflows

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-project
    with:
      node-version: '22'
  - run: npm test
```

## Secrets and Security

| Practice | Implementation |
|----------|---------------|
| Least privilege | Use fine-grained personal access tokens |
| Rotate secrets | Audit and rotate quarterly |
| Pin actions by SHA | `uses: actions/checkout@abcdef1` |
| Limit permissions | Add `permissions:` block to restrict GITHUB_TOKEN |

```yaml
permissions:
  contents: read
  pull-requests: write  # Only what's needed
```
