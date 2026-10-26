# Docker Best Practices

Patterns for building efficient, secure, and production-ready Docker images.

## Multi-Stage Builds

### Node.js Application

```dockerfile
# Stage 1: Install dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 appuser

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER appuser
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Why Multi-Stage

| Approach | Image Size | Build Cache | Security |
|----------|-----------|-------------|----------|
| Single stage | Large (1GB+) | Poor | Dev deps in prod |
| Multi-stage | Small (150-300MB) | Good | Only prod deps |
| Distroless | Smallest (50-100MB) | Good | Minimal attack surface |

## Image Optimization

### Layer ordering (most stable first)

```dockerfile
# 1. Base image (rarely changes)
FROM node:20-alpine

# 2. System dependencies (rarely changes)
RUN apk add --no-cache tini

# 3. Package files (changes when deps change)
COPY package.json package-lock.json ./

# 4. Install dependencies (cached until package files change)
RUN npm ci --omit=dev

# 5. Application code (changes most often)
COPY . .
```

### Reduce image size

```dockerfile
# Use alpine base images
FROM node:20-alpine  # ~180MB vs node:20 ~1GB

# Clean up in the same layer
RUN apk add --no-cache build-base python3 \
    && npm ci \
    && apk del build-base python3

# Use .dockerignore
# node_modules, .git, .env, *.md, tests/
```

### .dockerignore

```
node_modules
.git
.gitignore
.env
.env.*
*.md
tests/
coverage/
.next/
Dockerfile
docker-compose*.yml
.dockerignore
```

## Security

### Run as non-root

```dockerfile
RUN addgroup --system --gid 1001 app \
    && adduser --system --uid 1001 --ingroup app app

USER app
```

### Read-only filesystem

```yaml
# docker-compose.yml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

### Scan for vulnerabilities

```bash
# Docker Scout (built-in)
docker scout cves myimage:latest

# Trivy
trivy image myimage:latest

# Snyk
snyk container test myimage:latest
```

### Pin base image digests

```dockerfile
# Instead of :latest or :20
FROM node:20-alpine@sha256:abc123...
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

## Docker Compose Patterns

### Development environment

```yaml
services:
  app:
    build:
      context: .
      target: builder  # Use build stage for dev
    volumes:
      - .:/app
      - /app/node_modules  # Exclude node_modules from mount
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### Production with replicas

```yaml
services:
  app:
    image: ghcr.io/myorg/myapp:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: unless-stopped
```

## Build Arguments and Secrets

```dockerfile
# Build-time argument
ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine

# Build-time secret (not stored in image layers)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

```bash
docker build \
  --build-arg NODE_VERSION=22 \
  --secret id=npmrc,src=.npmrc \
  -t myapp .
```

## Container Logging

```dockerfile
# Log to stdout/stderr (Docker captures these)
CMD ["node", "server.js"]
# Do NOT log to files inside the container
```

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

## Graceful Shutdown

```dockerfile
# Use tini as init process for signal handling
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
```

```typescript
// In application code
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  await server.close();
  await db.disconnect();
  process.exit(0);
});
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `docker build -t app .` | Build image |
| `docker compose up -d` | Start services |
| `docker compose logs -f app` | Stream logs |
| `docker compose down -v` | Stop and remove volumes |
| `docker system prune -a` | Clean all unused resources |
| `docker stats` | Live resource usage |
