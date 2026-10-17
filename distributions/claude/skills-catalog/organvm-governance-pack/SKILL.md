---
name: organvm-governance-pack
description: Curated bundle of governance and quality skills for ORGANVM ecosystem management. Includes ecosystem autopsy and discovery, promotion readiness, onboarding flows, stranger testing, repository standards, verification, and coding standards. Use when establishing or auditing governance practices for repositories.
license: MIT
complexity: intermediate
time_to_learn: 5min
tags:
  - bundle
  - governance
  - quality
  - onboarding
  - promotion
  - autopsy
  - discovery
inputs:
  - repository-to-assess
outputs:
  - skill-bundle
includes:
  - ecosystem-autopsy
  - promotion-readiness-checklist
  - repo-onboarding-flow
  - stranger-test-protocol
  - github-repository-standards
  - verification-loop
  - coding-standards-enforcer
tier: core
governance_phases: [shape, prove]
governance_norm_group: quality-gate
organ_affinity: [all]
triggers: [context:new-repository, context:promotion-readiness, context:governance-review]
---

# ORGANVM Governance Pack

A curated bundle of skills for managing repository lifecycle, quality gates, and governance compliance across the ORGANVM ecosystem.

## What's Included

- **ecosystem-autopsy** — Discovery entrypoint. Orchestrate `organvm ecosystem` + `organvm irf` to surface unregistered repos and drift, then emit migration signals routing to downstream skills below
- **promotion-readiness-checklist** — Assess repositories against promotion state requirements (LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED)
- **repo-onboarding-flow** — Scaffold and integrate new repositories with seed.yaml, CI/CD, and documentation
- **stranger-test-protocol** — Validate that documentation is comprehensible to someone with zero context
- **github-repository-standards** — Enforce repository organization and README standards
- **verification-loop** — Comprehensive build/type/lint/test/security verification
- **coding-standards-enforcer** — Automated code style enforcement with linters and pre-commit hooks

## Getting Started

Install this bundle to establish governance practices across your repositories. The recommended workflow:

1. **Discovery:** Run ecosystem-autopsy to map the workspace, find unregistered repos, and emit drift signals
2. **New repos:** Use repo-onboarding-flow to scaffold and integrate
3. **Quality baseline:** Apply coding-standards-enforcer and verification-loop
4. **Documentation:** Run stranger-test-protocol to validate docs
5. **Promotion:** Use promotion-readiness-checklist to assess and advance governance state

This pack is designed for the ORGANVM eight-organ ecosystem but applies to any multi-repo system with governance requirements. Phase 1 (Discovery) feeds the downstream phases via the signal records ecosystem-autopsy emits.
