# Workflow Integration: Frontend Design Systems

This document describes how `frontend-design-systems` integrates with other skills in the Web Frontend Architecture ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `responsive-design-patterns` | **Downstream** | Apply tokens in responsive layouts |
| `accessibility-patterns` | **Downstream** | Verify token accessibility compliance |
| `web-artifacts-builder` | **Downstream** | Generate components from specifications |
| `nextjs-fullstack-patterns` | **Downstream** | Integrate design system in Next.js |

## Prerequisites

Before invoking `frontend-design-systems`, ensure:

1. **Brand identity defined** - Colors, typography preferences
2. **Component scope known** - What components are needed
3. **Technology stack decided** - CSS-in-JS, Tailwind, CSS modules

## Handoff Patterns

### To: responsive-design-patterns

**Trigger:** Tokens defined, need responsive behavior.

**What to hand off:**
- Spacing scale tokens
- Breakpoint definitions
- Container size tokens

**Expected output from responsive:**
- Media query patterns using tokens
- Container query implementations
- Fluid typography scales

### To: accessibility-patterns

**Trigger:** Components need accessibility validation.

**What to hand off:**
- Color palette with use cases
- Focus state definitions
- Interactive component specifications

**Expected output from accessibility:**
- Contrast ratio validation
- Focus ring specifications
- ARIA pattern requirements

### To: web-artifacts-builder

**Trigger:** Generate production components.

**What to hand off:**
- Component specifications
- Token values
- Variant definitions

**Expected output from artifacts:**
- React/TypeScript components
- Storybook stories
- Type definitions

### To: nextjs-fullstack-patterns

**Trigger:** Integrate design system into Next.js.

**What to hand off:**
- Token import patterns
- Component library structure
- Theme provider setup

**Expected output from nextjs:**
- Theme integration in layout
- Server/client component guidance
- CSS loading optimization

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Design System Creation                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. FRONTEND-DESIGN-SYSTEMS: Define tokens and components  │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  2a. RESPONSIVE-DESIGN-PATTERNS  2b. ACCESSIBILITY-PATTERNS│
│      (responsive tokens)             (a11y validation)     │
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

Before completing design system definition, verify:

- [ ] Color tokens have semantic names
- [ ] Typography scale is consistent
- [ ] Spacing follows a mathematical scale
- [ ] Breakpoints align with common devices
- [ ] Component variants are well-defined
- [ ] Token naming is systematic
- [ ] Dark mode tokens included
- [ ] Documentation generated

## Common Scenarios

### New Design System

1. **Frontend Design Systems:** Define complete token set
2. **Accessibility Patterns:** Validate contrast, focus states
3. **Responsive Design Patterns:** Add breakpoint tokens
4. **Web Artifacts Builder:** Generate component library

### Token Migration

1. **Frontend Design Systems:** Map old tokens to new
2. **Web Artifacts Builder:** Update components
3. **Next.js Fullstack Patterns:** Update theme provider

### Component Expansion

1. **Frontend Design Systems:** Design new component
2. **Accessibility Patterns:** Define ARIA requirements
3. **Responsive Design Patterns:** Add responsive variants
4. **Web Artifacts Builder:** Generate component

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded values | Inconsistent styling | Use tokens exclusively |
| Too many tokens | Decision paralysis | Follow design constraints |
| Missing dark mode | Poor user experience | Include from the start |
| No documentation | Difficult adoption | Generate docs with tokens |

## Related Resources

- [Web Frontend Skills Ecosystem Map](../../../docs/guides/web-frontend-skills-ecosystem.md)
- [Component Patterns Reference](./component-patterns.md)
