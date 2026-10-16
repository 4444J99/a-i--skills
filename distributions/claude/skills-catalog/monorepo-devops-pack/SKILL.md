---
name: monorepo-devops-pack
description: Curated bundle for managing monorepos with containerized deployment pipelines. Includes monorepo management, Docker containerization, CI/CD deployment, and coding standards. Use when setting up or improving multi-package repository infrastructure.
license: MIT
complexity: intermediate
time_to_learn: 5min
tags:
  - bundle
  - monorepo
  - devops
  - docker
  - ci-cd
inputs:
  - project-requirements
outputs:
  - skill-bundle
includes:
  - monorepo-management
  - docker-containerization
  - deployment-cicd
  - coding-standards-enforcer
tier: core
governance_phases: [shape, build]
organ_affinity: [organ-ii, organ-iii]
triggers: [context:monorepo-setup, context:devops-pipeline, context:multi-package]
---

# Monorepo DevOps Pack

A curated bundle for setting up and managing monorepo infrastructure with containerized deployment.

## What's Included

- **monorepo-management** — Workspace tools, dependency management, selective builds, and change detection with Turborepo/pnpm
- **docker-containerization** — Multi-stage Dockerfiles, Docker Compose, image optimization, and container security
- **deployment-cicd** — CI/CD pipelines with GitHub Actions, deployment strategies, and infrastructure as code
- **coding-standards-enforcer** — Automated code style enforcement with linters, formatters, and pre-commit hooks

## Getting Started

Install this bundle when setting up a monorepo with containerized deployment. The recommended sequence:

1. **Structure:** Use monorepo-management to set up workspaces and build tooling
2. **Standards:** Use coding-standards-enforcer for consistent style across all packages
3. **Containerize:** Use docker-containerization for production-ready images
4. **Deploy:** Use deployment-cicd to automate the build → test → deploy pipeline

This pack serves ORGAN-II (generative art multi-package repos) and ORGAN-III (commercial product monorepos).
