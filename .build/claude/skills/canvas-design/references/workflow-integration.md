# Workflow Integration: Canvas Design

This document describes how `canvas-design` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `algorithmic-art` | **Downstream** | Animate or generate from static design |
| `generative-art-algorithms` | **Downstream** | Generate variations algorithmically |
| `three-js-interactive-builder` | **Downstream** | Apply design in 3D scenes |
| `modular-synthesis-philosophy` | **Complementary** | Design thinking for systems |
| `narratological-algorithms` | **Complementary** | Visual narrative design |

## Prerequisites

Before invoking `canvas-design`, ensure:

1. **Brief defined** - Purpose and message of the design
2. **Constraints known** - Size, format, medium
3. **Assets available** - Typography, colors, imagery

## Handoff Patterns

### To: algorithmic-art

**Trigger:** Static design should become generative.

**What to hand off:**
- Color palette with relationships
- Composition grid or rules
- Typography specifications
- Visual language elements

**Expected output from algorithmic:**
- Animated version of design
- Generative variations
- Interactive elements

### To: generative-art-algorithms

**Trigger:** Create algorithmic variations.

**What to hand off:**
- Core visual elements
- Constraints for variations
- Acceptable parameter ranges

**Expected output from algorithms:**
- Parametric generation system
- Rule-based variations
- Batch generation capability

### To: three-js-interactive-builder

**Trigger:** Design principles applied to 3D.

**What to hand off:**
- Color system
- Composition principles
- Lighting mood references

**Expected output from three-js:**
- 3D environment with design coherence
- Material systems matching 2D
- Camera composition

### To: narratological-algorithms

**Trigger:** Design supports narrative.

**What to hand off:**
- Visual storytelling elements
- Information hierarchy
- Reading flow patterns

**Expected output from narrative:**
- Story pacing visualization
- Narrative beat design
- Visual story structure

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Design to Generative                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CANVAS-DESIGN: Create foundational design              │
│           │                                                 │
│           ├─────────────────────────────────────────┐       │
│           │             │             │             │       │
│           ▼             ▼             ▼             ▼       │
│      ALGORITHMIC   GEN-ART-ALG    THREE-JS    NARRATIVE    │
│          ART           ALG         BUILDER       ALG       │
│      (animate)      (generate)      (3D)       (story)     │
│           │             │             │             │       │
│           └─────────────┴─────────────┴─────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  2. Integrated outputs across media                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing canvas design, verify:

- [ ] Composition is balanced
- [ ] Color contrast is accessible
- [ ] Typography hierarchy clear
- [ ] Design scales appropriately
- [ ] Export formats prepared
- [ ] Design system documented
- [ ] Variations work at different sizes
- [ ] Dark mode version (if needed)

## Common Scenarios

### Brand Identity System

1. **Canvas Design:** Logo and core assets
2. **Generative Art Algorithms:** Parametric brand patterns
3. **Algorithmic Art:** Motion brand elements

### Print to Digital

1. **Canvas Design:** Print-first design
2. **Algorithmic Art:** Web/digital adaptation
3. **Three.js Interactive Builder:** Immersive version

### Data Visualization Style

1. **Canvas Design:** Visual style guide
2. **Generative Art Algorithms:** Chart generation system
3. **Three.js Interactive Builder:** 3D data viz

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No constraints | Inconsistent output | Define design system rules |
| Too many fonts | Visual chaos | Limit typographic palette |
| Poor contrast | Accessibility failure | Test color combinations |
| Not resolution-aware | Blurry output | Design for target resolutions |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
