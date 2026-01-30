# Feature Workflow Templates

Templates for managing feature development from ideation to deployment.

## Feature Specification Template

```markdown
# Feature: [Feature Name]

## Overview
- **Owner**: [Name]
- **Status**: Draft | In Review | Approved | In Progress | Done
- **Target Release**: [Version/Sprint]

## Problem Statement
What problem does this solve? Who experiences it?

## Proposed Solution
High-level description of the solution.

## User Stories
- As a [user type], I want [goal] so that [benefit]
- As a [user type], I want [goal] so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Approach
### Architecture
[Describe technical approach]

### Dependencies
- [ ] Dependency 1
- [ ] Dependency 2

### API Changes
[If applicable]

## Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| | | | |

## Timeline
| Phase | Duration | Start | End |
|-------|----------|-------|-----|
| Design | | | |
| Implementation | | | |
| Testing | | | |
| Rollout | | | |

## Success Metrics
- Metric 1: [Target]
- Metric 2: [Target]
```

## Git Branch Workflow

### Branch Naming

```
feature/TICKET-123-short-description
bugfix/TICKET-456-fix-login-error
hotfix/TICKET-789-critical-security-patch
release/v1.2.0
```

### Workflow Stages

```
main (production)
  │
  ├── develop (integration)
  │     │
  │     ├── feature/TICKET-123
  │     │     └── Commits...
  │     │
  │     ├── feature/TICKET-124
  │     │     └── Commits...
  │     │
  │     └── Merge back to develop
  │
  └── release/v1.2.0
        └── Merge to main + tag
```

## Pull Request Template

```markdown
## Description
[What does this PR do?]

## Related Issues
Closes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots
[If UI changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass locally
```

## Code Review Checklist

### For Reviewer

**Functionality**
- [ ] Code does what the PR description says
- [ ] Edge cases handled
- [ ] Error handling appropriate

**Code Quality**
- [ ] Code is readable and well-organized
- [ ] No unnecessary complexity
- [ ] DRY principles followed
- [ ] Naming is clear and consistent

**Testing**
- [ ] Tests cover the changes
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases tested

**Security**
- [ ] No sensitive data exposed
- [ ] Input validation present
- [ ] Authentication/authorization correct

**Performance**
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No memory leaks

### Review Response Guide

| Prefix | Meaning | Action Required |
|--------|---------|-----------------|
| `nit:` | Nitpick, minor | Optional |
| `suggestion:` | Consider this | Discuss |
| `question:` | Clarification needed | Respond |
| `issue:` | Problem found | Fix required |
| `blocker:` | Cannot merge until fixed | Fix required |

## Release Checklist

### Pre-Release
- [ ] All features complete and merged
- [ ] All tests passing
- [ ] Code review complete
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped

### Release
- [ ] Create release branch
- [ ] Final testing on release branch
- [ ] Create release tag
- [ ] Deploy to staging
- [ ] Smoke tests on staging
- [ ] Deploy to production

### Post-Release
- [ ] Monitor error rates
- [ ] Monitor performance metrics
- [ ] Verify feature flags
- [ ] Update project board
- [ ] Notify stakeholders
- [ ] Retrospective scheduled

## Feature Flag Template

```typescript
const featureFlags = {
  'new-checkout-flow': {
    enabled: false,
    rolloutPercentage: 0,
    allowList: ['user-123', 'user-456'],
    description: 'New streamlined checkout process'
  }
};

function isFeatureEnabled(flagName: string, userId: string): boolean {
  const flag = featureFlags[flagName];
  if (!flag) return false;

  // Check allowlist first
  if (flag.allowList.includes(userId)) return true;

  // Check if globally enabled
  if (!flag.enabled) return false;

  // Check rollout percentage
  const hash = hashUserId(userId);
  return hash < flag.rolloutPercentage;
}
```

## Status Definitions

| Status | Description |
|--------|-------------|
| **Backlog** | Captured but not prioritized |
| **Ready** | Prioritized and spec complete |
| **In Progress** | Actively being worked on |
| **In Review** | Code complete, awaiting review |
| **QA** | Review complete, in testing |
| **Ready to Deploy** | Tested, awaiting deployment |
| **Done** | Deployed to production |
| **Blocked** | Cannot progress, needs resolution |
