# Workflow Integration: Next.js Fullstack Patterns

This document describes how `nextjs-fullstack-patterns` integrates with other skills in the Web Frontend Architecture ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `frontend-design-systems` | **Upstream** | Integrate design system in layout |
| `responsive-design-patterns` | **Upstream** | Apply responsive patterns in pages |
| `accessibility-patterns` | **Upstream** | Ensure accessible page structure |
| `web-artifacts-builder` | **Upstream** | Receive generated components |

## Prerequisites

Before invoking `nextjs-fullstack-patterns`, ensure:

1. **Next.js version decided** - 13+ with App Router recommended
2. **Rendering strategy clear** - SSR, SSG, ISR, or client
3. **Data sources identified** - APIs, databases, external services

## Handoff Patterns

### From: frontend-design-systems

**Trigger:** Integrate design system into Next.js.

**What to receive:**
- Design token files
- Theme provider setup
- Global styles

**Integration points:**
- Configure theme in layout.tsx
- Set up CSS loading strategy
- Apply global tokens

### From: responsive-design-patterns

**Trigger:** Apply responsive patterns in pages.

**What to receive:**
- Page layout patterns
- Breakpoint-specific behavior
- Image sizing requirements

**Integration points:**
- Configure viewport meta
- Set up Next/Image responsive
- Apply page layouts

### From: accessibility-patterns

**Trigger:** Ensure accessible application structure.

**What to receive:**
- Landmark requirements
- Heading hierarchy
- Navigation patterns

**Integration points:**
- Set up skip links in layout
- Configure proper landmarks
- Implement accessible routing

### From: web-artifacts-builder

**Trigger:** Integrate generated components.

**What to receive:**
- React component files
- Type definitions
- Styling approach

**Integration points:**
- Decide server vs client components
- Configure component loading
- Set up data fetching

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Integration                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. NEXTJS-FULLSTACK-PATTERNS: Define architecture         │
│           │                                                 │
│           ▼                                                 │
│  2. FRONTEND-DESIGN-SYSTEMS: Provide design system         │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. RESPONSIVE-DESIGN-PATTERNS  3b. ACCESSIBILITY-PATTERNS│
│      (page layouts)                  (landmarks)           │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. WEB-ARTIFACTS-BUILDER: Generate page components        │
│           │                                                 │
│           ▼                                                 │
│  5. NEXTJS-FULLSTACK-PATTERNS: Wire up data + deploy       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing Next.js integration, verify:

- [ ] Server/client component boundaries clear
- [ ] Data fetching uses appropriate patterns
- [ ] Error boundaries in place
- [ ] Loading states implemented
- [ ] Metadata properly configured
- [ ] Image optimization enabled
- [ ] Route segments properly structured
- [ ] Environment variables secured

## Common Scenarios

### New Page Feature

1. **Next.js Fullstack Patterns:** Define route structure
2. **Frontend Design Systems:** Select components
3. **Web Artifacts Builder:** Generate page components
4. **Next.js Fullstack Patterns:** Add data fetching

### API Route Development

1. **Next.js Fullstack Patterns:** Define API route
2. **Next.js Fullstack Patterns:** Implement handler
3. **Web Artifacts Builder:** Create client components
4. **Accessibility Patterns:** Validate form handling

### Design System Integration

1. **Frontend Design Systems:** Export tokens and theme
2. **Next.js Fullstack Patterns:** Configure layout
3. **Responsive Design Patterns:** Apply breakpoints
4. **Web Artifacts Builder:** Generate themed components

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| All client components | No SSR benefits | Default to server, opt into client |
| Fetching in client | Waterfalls, poor UX | Fetch in server components |
| Missing loading.tsx | Poor perceived performance | Add loading UI |
| No error.tsx | Crashes break entire page | Implement error boundaries |

## Related Resources

- [Web Frontend Skills Ecosystem Map](../../../docs/guides/web-frontend-skills-ecosystem.md)
- [Next.js Patterns Reference](./nextjs-patterns.md)
