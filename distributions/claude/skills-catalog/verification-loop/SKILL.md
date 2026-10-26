---
name: verification-loop
description: Comprehensive quality verification system for code changes with build, type, lint, test, and security checks
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  adapted-by: ai-skills
  category: quality-assurance
governance_phases: [frame, prove]
governance_norm_group: quality-gate
governance_auto_activate: true
organ_affinity: [all]
triggers: [context:task-start, context:pre-commit, context:code-review, context:promotion]
complements: [testing-patterns, tdd-workflow, deployment-cicd]
---

# Verification Loop

A comprehensive verification system for ensuring code quality across multiple dimensions.

## When to Use

Invoke this skill:
- **At task start** — to declare the verification surface *before* writing code (Phase 0)
- After completing a feature or significant code change
- Before creating a pull request
- When you want to ensure quality gates pass
- After refactoring or major modifications
- During code review preparation

## Verification Phases

### Phase 0: Declare the verification surface (BEFORE any work)

Run this *before* writing code, not after. The other phases ratify finished work; this one decides — up front — how that work will be proven, and ensures the proof comes from outside the model.

State three things before starting:

1. **The external signal.** Name the concrete command or surface that will confirm success: a `Bash` test/lint/typecheck command, an MCP browser loading the real page and reading the DOM/console, a fresh session, or a second agent. "I'll review it myself when done" is **not** a verification surface.
2. **Why it is external to the generating context.** A self-check inside the same context that produced the code can ratify the very error that context introduced. The signal must come from outside that context — a process the model cannot silently satisfy by asserting success. (Origin failure mode: a model asked to fix a wrong display edited the *underlying value* and marked the task resolved — the system failed *and reported success*. Every phase below exists to make that signature visible; this phase makes it visible **before** it spreads.)
3. **If no surface exists, building it is part of the task.** Do not proceed to implementation until the signal is wired. The verification surface is a deliverable, not an afterthought.

> Declaration stamp: `Verify-by: <command/surface> — external? Y/N — exists yet? Y/N`. If `exists yet = N`, the first build step is to create it.

This is the forward-declaration that Phases 1–6 assume. It is the FRAME-phase half of this skill; Phases 1–6 are the PROVE-phase half. (Constitutional anchor: Reliquary Rule #64(c) "govern the model, don't execute through it"; operator-invoked equivalent: `/v-govern` step 3.)

### Phase 1: Build Verification
```bash
# Check if project builds
npm run build 2>&1 | tail -20
# OR
pnpm build 2>&1 | tail -20
# OR for other build systems
make build 2>&1 | tail -20
cargo build 2>&1 | tail -20
```

**Critical**: If build fails, STOP and fix before continuing.

### Phase 2: Type Check
```bash
# TypeScript projects
npx tsc --noEmit 2>&1 | head -30

# Python projects
pyright . 2>&1 | head -30
mypy . 2>&1 | head -30

# Go projects
go vet ./... 2>&1 | head -30
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint Check
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30
eslint . 2>&1 | head -30

# Python
ruff check . 2>&1 | head-30
flake8 . 2>&1 | head -30

# Go
golint ./... 2>&1 | head -30

# Rust
cargo clippy 2>&1 | head -30
```

### Phase 4: Test Suite
```bash
# Run tests with coverage
npm run test -- --coverage 2>&1 | tail -50
pytest --cov=. 2>&1 | tail -50
go test -cover ./... 2>&1 | tail -50

# Check coverage threshold
# Target: 80% minimum for new code
```

Report:
- Total tests: X
- Passed: X
- Failed: X
- Coverage: X%
- New files covered: X%

### Phase 5: Security Scan
```bash
# Check for secrets
grep -rn "sk-" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | head -10
grep -rn "password.*=" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | head -10

# Check for debug statements
grep -rn "console.log" --include="*.ts" --include="*.tsx" --include="*.js" src/ 2>/dev/null | head -10
grep -rn "print(" --include="*.py" . 2>/dev/null | head -10
grep -rn "println!" --include="*.rs" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review
```bash
# Show what changed
git diff --stat
git diff HEAD~1 --name-only
git diff --shortstat
```

Review each changed file for:
- Unintended changes or modifications
- Missing error handling
- Potential edge cases
- Documentation updates needed

## Output Format

After running all phases, produce a verification report:

```
VERIFICATION REPORT
==================

Build:     [✓ PASS / ✗ FAIL]
Types:     [✓ PASS / ✗ FAIL] (X errors)
Lint:      [✓ PASS / ✗ FAIL] (X warnings)
Tests:     [✓ PASS / ✗ FAIL] (X/Y passed, Z% coverage)
Security:  [✓ PASS / ✗ FAIL] (X issues)
Diff:      [X files changed, +Y lines, -Z lines]

Overall:   [✓ READY / ✗ NOT READY] for PR

Issues to Fix:
1. [Priority] Description
2. [Optional] Description
...

Recommendations:
- Suggestion 1
- Suggestion 2
```

## Continuous Mode

For long sessions, run verification every 15 minutes or after major changes:

**Checkpoints:**
- After completing each function
- After finishing a component
- Before moving to next task
- After resolving merge conflicts

## Integration Points

This skill complements:
- **testing-patterns**: For test design
- **deployment-cicd**: For CI pipeline preparation
- **github-repository-standards**: For PR preparation
- **security-threat-modeler**: For security review

## Quick Verification

For rapid checks during development:

```bash
# Minimal verification (30 seconds)
npm run build && npm run lint && npm test
```

Use full verification before commits.

---

## Related Skills

### Complementary Skills (Use Together)
- **[testing-patterns](../testing-patterns/)** - Comprehensive testing approaches for the test verification phase
- **[tdd-workflow](../tdd-workflow/)** - Test-driven development that produces code ready for verification
- **[deployment-cicd](../deployment-cicd/)** - CI pipelines that automate the verification loop

### Alternative Skills (Similar Purpose)
- None - verification-loop is a quality gate process, not an alternative to other practices

### Prerequisite Skills (Learn First)
- **[testing-patterns](../testing-patterns/)** - Understanding testing helps interpret verification results
