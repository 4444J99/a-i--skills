# Verification Checklist

Systematic verification steps for code changes.

## Pre-Commit Verification

### Code Quality

- [ ] Code compiles without errors
- [ ] No linting warnings
- [ ] Type checking passes
- [ ] Formatting is consistent

### Functionality

- [ ] Feature works as specified
- [ ] Edge cases handled
- [ ] Error states work correctly
- [ ] Loading states present

### Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] New tests added for new code
- [ ] Test coverage maintained

## Verification Loop Process

```
┌─────────────┐
│  Make Change │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  Run Tests  │────→│  Fix Issues │
└──────┬──────┘     └──────┬──────┘
       │                   │
       │ Pass              │
       ▼                   │
┌─────────────┐            │
│ Manual Check│←───────────┘
└──────┬──────┘
       │
       │ Works
       ▼
┌─────────────┐
│   Commit    │
└─────────────┘
```

## Automated Verification

### Pre-Commit Hooks

```bash
# .husky/pre-commit
#!/bin/sh
npm run lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --findRelatedTests"
    ]
  }
}
```

### CI Pipeline Checks

```yaml
# Essential checks
- lint: eslint, prettier
- typecheck: tsc --noEmit
- test: jest --coverage
- build: npm run build
- security: npm audit
```

## Manual Verification Steps

### Functional Testing

1. **Happy Path**
   - Does the primary use case work?
   - Is the output correct?

2. **Edge Cases**
   - Empty input
   - Maximum values
   - Minimum values
   - Invalid input

3. **Error Handling**
   - Network failures
   - Invalid data
   - Timeouts

### UI Verification

1. **Visual**
   - Layout correct
   - Responsive at all breakpoints
   - No visual regressions

2. **Interaction**
   - Click handlers work
   - Form submission works
   - Navigation correct

3. **Accessibility**
   - Keyboard navigation
   - Screen reader friendly
   - Focus management

## Verification by Change Type

### New Feature

- [ ] Feature spec reviewed
- [ ] All acceptance criteria met
- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] Documentation updated
- [ ] No performance regression

### Bug Fix

- [ ] Bug reproduced before fix
- [ ] Root cause identified
- [ ] Fix addresses root cause
- [ ] Regression test added
- [ ] Related areas checked
- [ ] Bug cannot be reproduced after fix

### Refactoring

- [ ] Behavior unchanged
- [ ] All existing tests pass
- [ ] No new features added
- [ ] Code is cleaner/simpler
- [ ] Performance maintained

### Dependency Update

- [ ] Changelog reviewed
- [ ] Breaking changes addressed
- [ ] All tests pass
- [ ] No security vulnerabilities
- [ ] Bundle size acceptable

## Quick Verification Commands

```bash
# TypeScript check
npx tsc --noEmit

# Lint
npm run lint

# Test
npm test

# Test with coverage
npm test -- --coverage

# Build
npm run build

# Security audit
npm audit
```

## Verification Failure Response

### Test Failure

1. Read the error message
2. Check if test is correct
3. Check if code is correct
4. Fix the actual problem
5. Re-run all tests

### Lint Failure

1. Run auto-fix: `npm run lint -- --fix`
2. Fix remaining issues manually
3. Verify no logical changes

### Type Error

1. Read the full error
2. Check expected vs actual type
3. Fix type or value
4. Ensure no `any` escape hatches

### Build Failure

1. Check for compile errors
2. Check for missing imports
3. Check for circular dependencies
4. Verify environment variables

## Post-Deployment Verification

- [ ] Health check endpoint responds
- [ ] Key user flows work
- [ ] No new errors in logs
- [ ] Performance metrics normal
- [ ] No alerts triggered

## Rollback Criteria

Rollback if any of these occur:
- Error rate > 1% (up from baseline)
- P99 latency > 2x baseline
- Critical user flow broken
- Security vulnerability detected
