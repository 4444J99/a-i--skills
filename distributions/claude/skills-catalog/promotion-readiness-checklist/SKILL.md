---
name: promotion-readiness-checklist
description: Assess repository readiness for promotion through governance states (LOCAL, CANDIDATE, PUBLIC_PROCESS, GRADUATED) with structured checklists, quality gates, and evidence requirements. Triggers on promotion assessment, readiness review, or governance state transition requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - promotion
  - governance
  - quality-gates
  - readiness
  - state-machine
governance_phases: [prove]
governance_norm_group: quality-gate
governance_auto_activate: true
organ_affinity: [all]
triggers: [user-asks-about-promotion, context:promotion-readiness, context:governance-state, context:quality-gate]
complements: [stranger-test-protocol, repo-onboarding-flow, verification-loop, coding-standards-enforcer]
---

# Promotion Readiness Checklist

Assess whether a repository meets the requirements for promotion to the next governance state.

## The Promotion State Machine

```
LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED
  ↓         ↓              ↓              ↓
 (no skip) (no skip)    (no skip)     (terminal)
```

**Hard rule:** No state skipping. Each transition requires explicit evidence of meeting all requirements.

## LOCAL → CANDIDATE

**Theme:** "This exists and has basic hygiene."

### Required

- [ ] **Repository exists** on GitHub with correct naming convention
- [ ] **seed.yaml** present with all required fields (schema_version, repo, organ, tier, promotion_status)
- [ ] **README.md** exists with ≥50 words explaining what this is
- [ ] **.gitignore** appropriate for the tech stack
- [ ] **LICENSE** file present (MIT for open, proprietary for internal)
- [ ] **No secrets committed** — checked with secret detection

### Evidence

```markdown
## LOCAL → CANDIDATE Evidence

- seed.yaml: ✓ (schema v1.0, organ: IV, tier: standard)
- README: ✓ (142 words)
- .gitignore: ✓ (Python template)
- LICENSE: ✓ (MIT)
- Secret scan: ✓ (clean)
- Date assessed: 2026-03-20
- Assessed by: {name/agent}
```

## CANDIDATE → PUBLIC_PROCESS

**Theme:** "This is tested, documented, and CI-verified."

### Required (all of LOCAL → CANDIDATE, plus)

- [ ] **CI pipeline** passing (lint + test on push/PR)
- [ ] **Tests exist** with ≥1 meaningful test
- [ ] **CLAUDE.md** or equivalent agent instructions present
- [ ] **Code linting** configured and passing (ruff, eslint, etc.)
- [ ] **Dependency management** configured (pyproject.toml, package.json)
- [ ] **Branch protection** enabled on main
- [ ] **At least one successful deployment** or release

### Quality Metrics

| Metric | Minimum | Target |
|--------|---------|--------|
| Test coverage | 30% | 60% |
| CI pass rate (30d) | 80% | 95% |
| Open issues | No blockers | All triaged |
| Documentation | README + CLAUDE.md | + Architecture doc |

### Evidence

```markdown
## CANDIDATE → PUBLIC_PROCESS Evidence

- CI: ✓ (GitHub Actions, 14/15 runs passed last 30 days = 93%)
- Tests: ✓ (12 tests, 45% coverage)
- CLAUDE.md: ✓ (includes dev commands, architecture, constraints)
- Linting: ✓ (ruff configured, 0 violations)
- Dependencies: ✓ (pyproject.toml with dev extras)
- Branch protection: ✓ (require PR, require CI)
- Deployment: ✓ (v0.1.0 released 2026-03-15)
```

## PUBLIC_PROCESS → GRADUATED

**Theme:** "This is production-quality and externally comprehensible."

### Required (all of CANDIDATE → PUBLIC_PROCESS, plus)

- [ ] **Stranger test passed** — documentation comprehensible to someone with zero context
- [ ] **Architecture documentation** with diagrams
- [ ] **CONTRIBUTING.md** with clear contribution guidelines
- [ ] **Error handling** comprehensive (no bare `except:` or swallowed errors)
- [ ] **Security review** completed (dependency audit, no known vulnerabilities)
- [ ] **Performance baseline** established (for applicable repos)
- [ ] **Monitoring/observability** in place (for applicable repos)
- [ ] **Inter-repo dependencies** documented in seed.yaml
- [ ] **All downstream consumers** identified and notified

### Quality Metrics

| Metric | Minimum | Target |
|--------|---------|--------|
| Test coverage | 60% | 80% |
| CI pass rate (30d) | 95% | 99% |
| Documentation score | 70% | 90% |
| Stranger test | Level 2 pass | Level 3 pass |
| Security audit | No critical | No high |

### Evidence

```markdown
## PUBLIC_PROCESS → GRADUATED Evidence

- Stranger test: ✓ (Level 3 pass, 2026-03-18)
- Architecture: ✓ (docs/architecture.md with Mermaid diagrams)
- CONTRIBUTING: ✓ (includes setup, PR process, coding standards)
- Error handling: ✓ (reviewed, no bare excepts)
- Security: ✓ (no critical/high vulnerabilities, last scanned 2026-03-19)
- Performance: ✓ (P99 < 200ms, baseline established)
- Dependencies: ✓ (seed.yaml edges match actual imports)
- Coverage: 72%
- CI pass rate: 97%
```

## GRADUATED → ARCHIVED

**Theme:** "This is no longer actively maintained."

### Required

- [ ] **Migration path** documented for consumers
- [ ] **Replacement identified** (if applicable)
- [ ] **Downstream consumers** migrated or notified
- [ ] **Final release** tagged
- [ ] **README** updated with archived status and redirect
- [ ] **GitHub repo** archived (read-only)

## Running the Assessment

### Automated Assessment Script

```python
def assess_promotion(repo_path: str, current_state: str, target_state: str) -> dict:
    checks = get_checks_for_transition(current_state, target_state)
    results = {}
    for check in checks:
        results[check.name] = check.evaluate(repo_path)

    passed = all(r["passed"] for r in results.values())
    return {
        "repo": repo_path,
        "transition": f"{current_state} → {target_state}",
        "passed": passed,
        "checks": results,
        "assessed_at": datetime.now().isoformat(),
    }
```

### Promotion Request Template

```markdown
## Promotion Request: {repo-name}

**Current state:** {state}
**Target state:** {state}
**Requested by:** {name}
**Date:** {date}

### Evidence
{Paste assessment output}

### Notes
{Any context about why this promotion is requested now}
```

## Anti-Patterns

- **Skipping states** — The state machine exists for a reason; shortcuts create gaps
- **Self-promotion without review** — At least one other person/agent should verify
- **Checking boxes without evidence** — Each check needs concrete evidence, not just ✓
- **Promoting to unblock** — Promotion signals quality; don't dilute it for convenience
- **No assessment record** — Keep evidence of every promotion decision for audit
- **One-time assessment** — Graduated repos can regress; periodic re-assessment is healthy
