# Workflow Integration: Web Artifacts Builder

This document describes how `web-artifacts-builder` integrates with other skills in the Web Frontend Architecture ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `frontend-design-systems` | **Upstream** | Receive component specifications |
| `responsive-design-patterns` | **Upstream** | Receive responsive requirements |
| `accessibility-patterns` | **Upstream** | Receive ARIA and keyboard patterns |
| `nextjs-fullstack-patterns` | **Downstream** | Integrate artifacts into Next.js |

## Prerequisites

Before invoking `web-artifacts-builder`, ensure:

1. **Component specifications defined** - Props, variants, behavior
2. **Design tokens available** - Colors, spacing, typography
3. **Accessibility requirements known** - ARIA, keyboard handling

## Handoff Patterns

### From: frontend-design-systems

**Trigger:** Component specifications ready for implementation.

**What to receive:**
- Component API definition (props, variants)
- Design tokens to use
- Composition patterns

**Integration points:**
- Map tokens to styled components
- Implement variants
- Generate prop types

### From: responsive-design-patterns

**Trigger:** Components need responsive behavior.

**What to receive:**
- Responsive prop specifications
- Breakpoint-specific behavior
- Container query requirements

**Integration points:**
- Add responsive props
- Implement media queries
- Add container query styles

### From: accessibility-patterns

**Trigger:** Components need accessibility implementation.

**What to receive:**
- ARIA role and attribute specifications
- Keyboard interaction patterns
- Focus management requirements

**Integration points:**
- Add ARIA attributes
- Implement keyboard handlers
- Manage focus programmatically

### To: nextjs-fullstack-patterns

**Trigger:** Artifacts ready for Next.js integration.

**What to hand off:**
- React component files
- TypeScript type definitions
- CSS/styled components

**Expected output from nextjs:**
- Server/client component decisions
- Page integration patterns
- Data fetching for components

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Component Generation                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. FRONTEND-DESIGN-SYSTEMS: Component specification       │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  2a. RESPONSIVE-DESIGN-PATTERNS  2b. ACCESSIBILITY-PATTERNS│
│      (responsive specs)              (ARIA specs)          │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  3. WEB-ARTIFACTS-BUILDER: Generate components             │
│           │                                                 │
│           ▼                                                 │
│  4. NEXTJS-FULLSTACK-PATTERNS: Integrate in app            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing artifact generation, verify:

- [ ] All props properly typed with TypeScript
- [ ] Responsive props work at all breakpoints
- [ ] ARIA attributes correctly applied
- [ ] Keyboard interactions implemented
- [ ] Focus management handles edge cases
- [ ] Tokens used instead of hardcoded values
- [ ] Component is properly tree-shakeable
- [ ] Storybook story included

## Common Scenarios

### Design System Component

1. **Frontend Design Systems:** Define component spec
2. **Accessibility Patterns:** Add ARIA requirements
3. **Responsive Design Patterns:** Add responsive behavior
4. **Web Artifacts Builder:** Generate component

### Interactive Widget

1. **Web Artifacts Builder:** Generate base structure
2. **Accessibility Patterns:** Add keyboard handling
3. **Responsive Design Patterns:** Mobile interactions
4. **Next.js Fullstack Patterns:** Client component wrapper

### Data-Driven Component

1. **Next.js Fullstack Patterns:** Define data requirements
2. **Web Artifacts Builder:** Generate presentation layer
3. **Accessibility Patterns:** Add live region updates

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Inline styles | Can't use tokens | Use CSS modules or styled-components |
| Missing types | Type errors at runtime | Full TypeScript coverage |
| No variants | Inflexible components | Design with variants upfront |
| Monolithic components | Hard to maintain | Compose smaller pieces |

## Related Resources

- [Web Frontend Skills Ecosystem Map](../../../docs/guides/web-frontend-skills-ecosystem.md)
- [Artifact Patterns Reference](./artifact-patterns.md)
