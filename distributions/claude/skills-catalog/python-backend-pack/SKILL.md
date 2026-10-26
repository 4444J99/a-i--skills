---
name: python-backend-pack
description: Curated bundle of essential Python backend development skills. Includes FastAPI patterns, packaging, database migrations, CLI design, and Redis caching. Use when building Python API services or backend systems.
license: MIT
complexity: intermediate
time_to_learn: 5min
tags:
  - bundle
  - python
  - backend
  - api
  - infrastructure
inputs:
  - project-requirements
outputs:
  - skill-bundle
includes:
  - fastapi-patterns
  - python-packaging-patterns
  - database-migration-patterns
  - cli-tool-design
  - redis-patterns
tier: core
governance_phases: [build]
organ_affinity: [organ-iii, organ-iv, meta]
triggers: [context:python-backend, context:python-api, context:new-python-project]
---

# Python Backend Pack

A curated bundle of essential skills for building Python backend services — from project structure through API, database, caching, and CLI.

## What's Included

- **fastapi-patterns** — Production FastAPI applications with async patterns, dependency injection, and Pydantic models
- **python-packaging-patterns** — Project structure, pyproject.toml, dependency management, and distribution
- **database-migration-patterns** — Safe schema evolution with Alembic, zero-downtime strategies, and rollback
- **cli-tool-design** — Command-line interfaces with Typer/Click, subcommands, and shell completion
- **redis-patterns** — Caching, pub/sub messaging, rate limiting, and distributed locks

## Getting Started

Install this bundle when starting a Python backend project. The recommended sequence:

1. **Structure:** Use python-packaging-patterns to set up pyproject.toml and project layout
2. **API:** Use fastapi-patterns for async API endpoints with Pydantic validation
3. **Database:** Use database-migration-patterns for schema management with Alembic
4. **Caching:** Use redis-patterns for caching and rate limiting layers
5. **CLI:** Use cli-tool-design for management commands and operational tooling

This pack covers the core Python backend stack used across ORGAN-III (commerce), ORGAN-IV (orchestration), and META-ORGANVM.
