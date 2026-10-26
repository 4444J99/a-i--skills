---
name: docker-containerization
description: Containerize applications with multi-stage Dockerfiles, Docker Compose orchestration, image optimization, and container security. Covers Python, Node.js, and multi-service architectures. Triggers on Docker, containerization, or container orchestration requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - docker
  - containers
  - docker-compose
  - multi-stage-build
  - devops
governance_phases: [build, prove]
governance_norm_group: distribution-readiness
organ_affinity: [organ-ii, organ-iii, meta]
triggers: [user-asks-about-docker, project-has-dockerfile, project-has-docker-compose, context:containerization, context:deployment]
complements: [deployment-cicd, python-packaging-patterns, resilience-patterns]
---

# Docker Containerization

Build efficient, secure container images and compose multi-service architectures.

## Multi-Stage Builds

### Python Application

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

# Stage 2: Runtime
FROM python:3.12-slim
COPY --from=builder /install /usr/local
COPY src/ /app/src/
WORKDIR /app
USER nobody
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Node.js Application

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Image Optimization

### Layer Ordering

Order instructions from least to most frequently changing:

```dockerfile
FROM python:3.12-slim
# 1. System deps (rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && rm -rf /var/lib/apt/lists/*
# 2. Python deps (change occasionally)
COPY pyproject.toml .
RUN pip install --no-cache-dir .
# 3. Application code (changes often)
COPY src/ ./src/
```

### Size Reduction

| Technique | Savings |
|-----------|---------|
| Alpine/slim base | 50-80% |
| Multi-stage builds | 40-70% |
| `--no-cache-dir` for pip | 10-20% |
| `.dockerignore` | Variable |
| Combine RUN layers | 5-15% |

### .dockerignore

```
.git
.venv
__pycache__
*.pyc
node_modules
.env
*.md
tests/
docs/
.build/
```

## Docker Compose

### Multi-Service Architecture

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

volumes:
  pgdata:
```

### Development Overrides

```yaml
# docker-compose.override.yml (auto-loaded in dev)
services:
  api:
    build:
      context: .
      target: builder
    volumes:
      - ./src:/app/src:ro
    command: ["python", "-m", "uvicorn", "src.app:app", "--reload", "--host", "0.0.0.0"]
    environment:
      - DEBUG=1
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

```python
# Minimal health endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
```

## Container Security

### Non-Root Execution

```dockerfile
# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 appuser --ingroup appgroup
USER appuser
```

### Read-Only Filesystem

```yaml
services:
  api:
    read_only: true
    tmpfs:
      - /tmp
      - /app/cache
```

### Secrets Management

```yaml
services:
  api:
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Scanning

```bash
# Scan for vulnerabilities
docker scout cves myimage:latest
trivy image myimage:latest
```

## Common Patterns

### Wait for Dependencies

```bash
#!/usr/bin/env bash
set -euo pipefail

# wait-for-it pattern
until pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  echo "Waiting for database..."
  sleep 2
done

exec "$@"
```

```dockerfile
COPY scripts/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "src.app:app"]
```

### Build Arguments

```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ARG BUILD_DATE
ARG GIT_SHA
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${GIT_SHA}"
```

```bash
docker build \
  --build-arg BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --build-arg GIT_SHA=$(git rev-parse HEAD) \
  -t myapp:latest .
```

## Anti-Patterns

- **Running as root** — Always use a non-root USER
- **Using `latest` tag in production** — Pin specific versions
- **Storing secrets in images** — Use runtime secrets or environment variables
- **One process per container violated** — Keep containers single-purpose
- **No .dockerignore** — Always exclude .git, node_modules, .venv, tests
- **Installing dev dependencies in prod image** — Use multi-stage builds to separate
