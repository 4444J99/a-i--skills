# CI/CD Pipeline Templates

Ready-to-use pipeline configurations for common scenarios.

## GitHub Actions

### Node.js CI

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

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build --if-present
      - run: npm test

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
```

### Deploy to Vercel

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Docker Build & Push

```yaml
name: Docker

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Release with Semantic Versioning

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

## GitLab CI

### Node.js Pipeline

```yaml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test

deploy:
  stage: deploy
  image: node:${NODE_VERSION}
  script:
    - npm run deploy
  only:
    - main
  environment:
    name: production
```

## Common Pipeline Stages

### Standard Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Build   │ -> │   Test   │ -> │  Deploy  │ -> │  Verify  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Detailed Stages

| Stage | Actions |
|-------|---------|
| **Install** | Install dependencies, cache |
| **Lint** | ESLint, Prettier, TypeCheck |
| **Build** | Compile, bundle |
| **Test** | Unit, integration tests |
| **Security** | Dependency audit, SAST |
| **Deploy Staging** | Deploy to staging |
| **E2E Test** | End-to-end tests |
| **Deploy Prod** | Deploy to production |
| **Verify** | Smoke tests, monitoring |

## Environment Variables

### Secrets Management

```yaml
# GitHub Actions
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# GitLab CI (Settings > CI/CD > Variables)
variables:
  DATABASE_URL: ${DATABASE_URL}
```

### Common Variables

| Variable | Purpose |
|----------|---------|
| `NODE_ENV` | production/development |
| `CI` | true in CI environment |
| `DATABASE_URL` | Database connection |
| `DEPLOY_TOKEN` | Deployment auth |
| `SENTRY_DSN` | Error tracking |

## Deployment Strategies

### Blue-Green

```yaml
deploy:
  script:
    - deploy_to_green
    - run_smoke_tests
    - switch_traffic_to_green
    - if_failed: rollback_to_blue
```

### Canary

```yaml
deploy:
  script:
    - deploy_canary  # 5% traffic
    - monitor_errors (5min)
    - if_healthy: increase_to_25
    - monitor_errors (5min)
    - if_healthy: increase_to_100
```

### Rolling

```yaml
deploy:
  script:
    - for instance in $INSTANCES:
        - drain_traffic $instance
        - deploy $instance
        - health_check $instance
        - resume_traffic $instance
```

## Caching Strategies

### npm/yarn

```yaml
# GitHub Actions
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: npm-

# GitLab CI
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
```

### Docker Layer Caching

```yaml
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Pipeline Best Practices

1. **Fail fast**: Run quick checks (lint) before slow ones (e2e)
2. **Parallel when possible**: Independent stages run together
3. **Cache aggressively**: Dependencies, build artifacts
4. **Use matrix builds**: Test across versions
5. **Keep secrets secret**: Use encrypted variables
6. **Artifact important outputs**: Build results, test reports
7. **Add timeouts**: Prevent hanging pipelines
8. **Notify on failure**: Slack, email, etc.
