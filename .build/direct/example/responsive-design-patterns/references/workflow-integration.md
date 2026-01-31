# Workflow Integration: Responsive Design Patterns

This document describes how `responsive-design-patterns` integrates with other skills in the Web Frontend Architecture ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `frontend-design-systems` | **Upstream** | Receive spacing and breakpoint tokens |
| `accessibility-patterns` | **Complementary** | Ensure responsive layouts remain accessible |
| `web-artifacts-builder` | **Downstream** | Generate responsive components |
| `nextjs-fullstack-patterns` | **Downstream** | Apply responsive patterns in Next.js pages |

## Prerequisites

Before invoking `responsive-design-patterns`, ensure:

1. **Design tokens exist** - Spacing and breakpoint values
2. **Content requirements known** - What content must adapt
3. **Target devices identified** - Mobile, tablet, desktop ranges

## Handoff Patterns

### From: frontend-design-systems

**Trigger:** Need to apply tokens in responsive contexts.

**What to receive:**
- Spacing scale tokens
- Breakpoint definitions
- Typography tokens with scales

**Integration points:**
- Map tokens to media query values
- Apply spacing in layout calculations
- Use fluid typography formulas

### To: accessibility-patterns

**Trigger:** Responsive layouts need accessibility validation.

**What to hand off:**
- Layout patterns at each breakpoint
- Touch target sizing
- Reflow behavior

**Expected output from accessibility:**
- 400% zoom compliance
- Touch target verification (48px min)
- Orientation handling

### To: web-artifacts-builder

**Trigger:** Generate responsive React components.

**What to hand off:**
- Responsive prop specifications
- Breakpoint behavior definitions
- Container query requirements

**Expected output from artifacts:**
- Components with responsive props
- CSS with media/container queries
- Responsive utility components

### To: nextjs-fullstack-patterns

**Trigger:** Apply responsive patterns in Next.js pages.

**What to hand off:**
- Page layout patterns
- Image optimization requirements
- SSR considerations for responsive

**Expected output from nextjs:**
- Responsive page layouts
- Next/Image responsive configurations
- Dynamic viewport handling

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Responsive Implementation                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. FRONTEND-DESIGN-SYSTEMS: Provide spacing/breakpoints   │
│           │                                                 │
│           ▼                                                 │
│  2. RESPONSIVE-DESIGN-PATTERNS: Design adaptive layouts    │
│           │                                                 │
│           ▼                                                 │
│  3. ACCESSIBILITY-PATTERNS: Verify reflow and targets      │
│           │                                                 │
│           ▼                                                 │
│  4. WEB-ARTIFACTS-BUILDER: Generate responsive components  │
│           │                                                 │
│           ▼                                                 │
│  5. NEXTJS-FULLSTACK-PATTERNS: Integrate in pages          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing responsive implementation, verify:

- [ ] All breakpoints tested with real content
- [ ] Touch targets meet 48x48px minimum
- [ ] No horizontal scroll on any breakpoint
- [ ] Text remains readable without zoom
- [ ] Images scale appropriately
- [ ] Navigation adapts to screen size
- [ ] Forms remain usable on mobile
- [ ] 400% zoom doesn't break layout

## Common Scenarios

### Mobile-First Component

1. **Frontend Design Systems:** Define breakpoint tokens
2. **Responsive Design Patterns:** Design mobile-first layout
3. **Accessibility Patterns:** Verify touch targets
4. **Web Artifacts Builder:** Generate component

### Complex Layout Grid

1. **Responsive Design Patterns:** Define grid at breakpoints
2. **Frontend Design Systems:** Add grid tokens
3. **Web Artifacts Builder:** Generate grid component
4. **Next.js Fullstack Patterns:** Apply in page layouts

### Responsive Images

1. **Responsive Design Patterns:** Define image sizing rules
2. **Next.js Fullstack Patterns:** Configure Next/Image
3. **Accessibility Patterns:** Add alt text guidance

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Desktop-first | Mobile afterthought | Start mobile-first |
| Fixed breakpoints | Doesn't match content | Content-based breakpoints |
| Hidden content | Poor mobile UX | Adapt, don't hide |
| No container queries | Component-unaware | Use container queries for components |

## Related Resources

- [Web Frontend Skills Ecosystem Map](../../../docs/guides/web-frontend-skills-ecosystem.md)
- [Breakpoint Patterns Reference](./breakpoint-patterns.md)
