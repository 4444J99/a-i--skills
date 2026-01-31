# Workflow Integration: Algorithmic Art

This document describes how `algorithmic-art` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `canvas-design` | **Upstream** | Receive composition and color foundations |
| `modular-synthesis-philosophy` | **Upstream** | Apply modular signal-flow thinking |
| `generative-art-algorithms` | **Downstream** | Advanced mathematical patterns |
| `three-js-interactive-builder` | **Downstream** | Extend patterns to 3D |
| `generative-music-composer` | **Complementary** | Audio-reactive visuals |

## Prerequisites

Before invoking `algorithmic-art`, ensure:

1. **Visual concept defined** - What should the art communicate
2. **Technical constraints known** - Canvas size, frame rate, platform
3. **Interactivity requirements** - Static, reactive, or generative

## Handoff Patterns

### From: canvas-design

**Trigger:** Static design needs to become generative.

**What to receive:**
- Color palette and ratios
- Composition grid or rules
- Typography specifications

**Integration points:**
- Convert colors to parametric systems
- Animate composition rules
- Create kinetic typography

### From: modular-synthesis-philosophy

**Trigger:** System design for generative visual.

**What to receive:**
- Signal flow concepts
- Modular architecture patterns
- Feedback and control ideas

**Integration points:**
- Design modular visual components
- Implement data flow between elements
- Create feedback loops

### To: generative-art-algorithms

**Trigger:** Need more sophisticated mathematical patterns.

**What to hand off:**
- Current pattern approaches
- Desired complexity level
- Performance constraints

**Expected output from algorithms:**
- Mathematical pattern definitions
- Optimized implementations
- Parametric controls

### To: three-js-interactive-builder

**Trigger:** Pattern needs 3D implementation.

**What to hand off:**
- Pattern logic and parameters
- Visual language established
- Interaction patterns

**Expected output from three-js:**
- 3D scene implementation
- Shader translations
- Interactive controls

### To: generative-music-composer

**Trigger:** Visuals should respond to or generate audio.

**What to hand off:**
- Visual parameter ranges
- Update timing requirements
- Sync points

**Expected output from music:**
- Audio analysis integration
- Beat detection callbacks
- Frequency band mappings

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Algorithmic Art Creation                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CANVAS-DESIGN or MODULAR-SYNTHESIS: Foundation         │
│           │                                                 │
│           ▼                                                 │
│  2. ALGORITHMIC-ART: Create generative patterns            │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. GENERATIVE-ART-ALGORITHMS  3b. THREE-JS-BUILDER       │
│      (mathematical depth)           (3D extension)         │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. GENERATIVE-MUSIC-COMPOSER: Audio integration           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing algorithmic art, verify:

- [ ] Pattern is visually coherent
- [ ] Performance is acceptable (60fps target)
- [ ] Parameters are exposed for variation
- [ ] Random seeds allow reproducibility
- [ ] Canvas/viewport sizing handled
- [ ] Export options available (PNG, SVG, video)
- [ ] Interaction patterns work smoothly
- [ ] Color accessibility considered

## Common Scenarios

### Generative Identity System

1. **Canvas Design:** Brand colors and composition
2. **Algorithmic Art:** Generative pattern system
3. **Generative Art Algorithms:** Refine for variations

### Audio-Reactive Visual

1. **Modular Synthesis Philosophy:** Signal flow design
2. **Algorithmic Art:** Visual response system
3. **Generative Music Composer:** Audio analysis

### Installation Piece

1. **Algorithmic Art:** Core pattern system
2. **Three.js Interactive Builder:** 3D environment
3. **Generative Music Composer:** Synchronized audio

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded colors | No variation | Use parametric color systems |
| Fixed canvas size | Doesn't adapt | Responsive canvas sizing |
| No seed control | Can't reproduce | Expose random seeds |
| Heavy draw loop | Poor performance | Optimize rendering |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
