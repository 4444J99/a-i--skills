# Workflow Integration: Generative Art Algorithms

This document describes how `generative-art-algorithms` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `algorithmic-art` | **Upstream** | Receive pattern concepts to formalize |
| `modular-synthesis-philosophy` | **Upstream** | Apply system thinking |
| `three-js-interactive-builder` | **Downstream** | Implement algorithms in 3D |
| `canvas-design` | **Complementary** | Apply to static outputs |
| `generative-music-composer` | **Complementary** | Algorithmic music patterns |

## Prerequisites

Before invoking `generative-art-algorithms`, ensure:

1. **Mathematical domain identified** - Noise, fractals, cellular automata, etc.
2. **Visual goal clear** - What aesthetic to achieve
3. **Performance constraints known** - Real-time vs. pre-rendered

## Handoff Patterns

### From: algorithmic-art

**Trigger:** Pattern needs mathematical sophistication.

**What to receive:**
- Current pattern approach
- Desired complexity
- Visual examples or references

**Integration points:**
- Formalize pattern mathematically
- Optimize algorithms
- Add parametric controls

### From: modular-synthesis-philosophy

**Trigger:** System architecture for complex generation.

**What to receive:**
- Modular architecture concepts
- Signal flow patterns
- State machine designs

**Integration points:**
- Design algorithm modules
- Connect generation stages
- Implement feedback systems

### To: three-js-interactive-builder

**Trigger:** Algorithm needs 3D implementation.

**What to hand off:**
- Algorithm definitions
- Parameter mappings
- Performance characteristics

**Expected output from three-js:**
- Shader implementations
- Geometry generation
- 3D visualization

### To: canvas-design

**Trigger:** Generate static outputs.

**What to hand off:**
- Generation parameters for static output
- Color scheme from algorithm
- Composition derived from rules

**Expected output from canvas:**
- Export-ready compositions
- Print specifications
- Asset versions

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Algorithm Development                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MODULAR-SYNTHESIS or ALGORITHMIC-ART: Concept          │
│           │                                                 │
│           ▼                                                 │
│  2. GENERATIVE-ART-ALGORITHMS: Formalize mathematically    │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. THREE-JS-BUILDER          3b. CANVAS-DESIGN           │
│      (3D implementation)           (static outputs)        │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. Final outputs: real-time or rendered                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing algorithm work, verify:

- [ ] Algorithm is mathematically sound
- [ ] Edge cases handled (division by zero, etc.)
- [ ] Parameters have sensible ranges
- [ ] Performance tested at target resolution
- [ ] Deterministic given same inputs
- [ ] Documentation of algorithm logic
- [ ] Visual results match intent
- [ ] Memory usage acceptable

## Common Scenarios

### Noise-Based Generative Art

1. **Algorithmic Art:** Initial noise pattern concept
2. **Generative Art Algorithms:** Layered noise implementation
3. **Three.js Interactive Builder:** Real-time visualization

### Fractal Generation

1. **Generative Art Algorithms:** Fractal math implementation
2. **Canvas Design:** High-resolution static renders
3. **Three.js Interactive Builder:** Interactive exploration

### Cellular Automata

1. **Modular Synthesis Philosophy:** Rule design approach
2. **Generative Art Algorithms:** Automaton implementation
3. **Generative Music Composer:** Sonification of states

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Infinite loops | Crashes | Add iteration limits |
| Floating point drift | Visual artifacts | Use appropriate precision |
| No bounds checking | Edge case crashes | Validate all inputs |
| Premature optimization | Hard to modify | Optimize after correctness |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
