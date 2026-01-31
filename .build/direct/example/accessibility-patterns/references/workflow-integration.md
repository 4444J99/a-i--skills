# Workflow Integration: Accessibility Patterns

This document describes how `accessibility-patterns` integrates with other skills in the Web Frontend Architecture ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `frontend-design-systems` | **Upstream** | Validate token accessibility (contrast, focus) |
| `responsive-design-patterns` | **Complementary** | Ensure responsive designs are accessible |
| `web-artifacts-builder` | **Downstream** | Generate accessible components |
| `nextjs-fullstack-patterns` | **Downstream** | Apply accessibility in Next.js |

## Prerequisites

Before invoking `accessibility-patterns`, ensure:

1. **WCAG level target known** - A, AA, or AAA
2. **User needs identified** - Visual, motor, cognitive considerations
3. **Testing tools available** - Screen reader, contrast checker

## Handoff Patterns

### From: frontend-design-systems

**Trigger:** Tokens need accessibility validation.

**What to receive:**
- Color palette with intended uses
- Focus state definitions
- Typography scale

**Integration points:**
- Validate color contrast ratios
- Design focus indicators
- Verify text size minimums

### From: responsive-design-patterns

**Trigger:** Responsive layouts need accessibility review.

**What to receive:**
- Layout patterns at breakpoints
- Touch target dimensions
- Reflow behavior

**Integration points:**
- Verify 400% zoom compliance
- Validate touch target sizes
- Check orientation handling

### To: web-artifacts-builder

**Trigger:** Generate accessible components.

**What to hand off:**
- ARIA role specifications
- Keyboard interaction patterns
- Focus management requirements

**Expected output from artifacts:**
- Accessible React components
- ARIA attributes implemented
- Keyboard handlers included

### To: nextjs-fullstack-patterns

**Trigger:** Apply accessibility in Next.js application.

**What to hand off:**
- Page structure requirements (landmarks)
- Navigation accessibility patterns
- Form validation accessibility

**Expected output from nextjs:**
- Accessible route structure
- Proper heading hierarchy
- Accessible forms

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Accessibility Integration                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. FRONTEND-DESIGN-SYSTEMS: Provide color/focus tokens    │
│           │                                                 │
│           ▼                                                 │
│  2. ACCESSIBILITY-PATTERNS: Validate and enhance           │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. Validate RESPONSIVE layouts  3b. Define ARIA patterns │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. WEB-ARTIFACTS-BUILDER: Generate accessible components  │
│           │                                                 │
│           ▼                                                 │
│  5. NEXTJS-FULLSTACK-PATTERNS: Integrate accessibly        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing accessibility implementation, verify:

- [ ] Color contrast meets WCAG requirements (4.5:1 normal, 3:1 large)
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible and clear
- [ ] ARIA labels on all controls
- [ ] Error messages announced to screen readers
- [ ] Skip links for main content
- [ ] Proper heading hierarchy
- [ ] Alt text for all images

## Common Scenarios

### Component Accessibility Audit

1. **Accessibility Patterns:** Identify violations
2. **Frontend Design Systems:** Update tokens
3. **Web Artifacts Builder:** Regenerate components
4. **Next.js Fullstack Patterns:** Deploy updates

### New Accessible Component

1. **Frontend Design Systems:** Define component
2. **Accessibility Patterns:** Specify ARIA requirements
3. **Web Artifacts Builder:** Generate with accessibility
4. **Accessibility Patterns:** Test with assistive tech

### Form Accessibility

1. **Accessibility Patterns:** Define form patterns
2. **Responsive Design Patterns:** Mobile form layout
3. **Web Artifacts Builder:** Generate form components
4. **Next.js Fullstack Patterns:** Server-side validation

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Relying on color alone | Colorblind users excluded | Add icons, text, patterns |
| Missing focus states | Keyboard users lost | Visible focus indicators |
| Div buttons | Not keyboard accessible | Use semantic `<button>` |
| Auto-playing media | Disorienting | Require user interaction |

## Related Resources

- [Web Frontend Skills Ecosystem Map](../../../docs/guides/web-frontend-skills-ecosystem.md)
- [WCAG Checklist Reference](./wcag-checklist.md)
