# Workflow Integration: Modular Synthesis Philosophy

This document describes how `modular-synthesis-philosophy` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `generative-music-composer` | **Downstream** | Apply to audio system design |
| `algorithmic-art` | **Downstream** | Apply to visual system design |
| `generative-art-algorithms` | **Downstream** | Inform algorithm architecture |
| `three-js-interactive-builder` | **Downstream** | Scene system architecture |
| `narratological-algorithms` | **Complementary** | Story as modular system |

## Prerequisites

Before invoking `modular-synthesis-philosophy`, ensure:

1. **System scope understood** - What is being designed
2. **Flexibility requirements known** - How modular must it be
3. **Complexity level identified** - Simple patch vs. complex graph

## Handoff Patterns

### To: generative-music-composer

**Trigger:** Design audio generation architecture.

**What to hand off:**
- Signal flow paradigm
- Module connection patterns
- Control voltage concepts

**Expected output from composer:**
- Audio module implementations
- Patch-based music system
- Parameter routing

### To: algorithmic-art

**Trigger:** Design visual generation architecture.

**What to hand off:**
- Data flow patterns
- Modular visual components
- Feedback loop concepts

**Expected output from algorithmic:**
- Visual module system
- Patchable parameters
- Signal-based animation

### To: generative-art-algorithms

**Trigger:** Architecture for complex algorithm.

**What to hand off:**
- Module decomposition approach
- State management pattern
- Composition strategies

**Expected output from algorithms:**
- Modular algorithm structure
- Composable functions
- Clear interfaces

### To: three-js-interactive-builder

**Trigger:** Scene architecture design.

**What to hand off:**
- System graph concepts
- Entity-component thinking
- Signal routing patterns

**Expected output from three-js:**
- Modular scene architecture
- Component-based entities
- Data-driven behavior

### To: narratological-algorithms

**Trigger:** Story as modular system.

**What to hand off:**
- State machine concepts
- Module connection patterns
- Recombination ideas

**Expected output from narrative:**
- Modular story components
- Recombinatorial narrative
- State-based progression

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Modular System Design                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MODULAR-SYNTHESIS-PHILOSOPHY: Define system approach   │
│           │                                                 │
│           ├─────────────────────────────────────────┐       │
│           │             │             │             │       │
│           ▼             ▼             ▼             ▼       │
│      GEN-MUSIC    ALGORITHMIC    GEN-ART-ALG    THREE-JS   │
│      COMPOSER         ART            ALG         BUILDER   │
│           │             │             │             │       │
│           └─────────────┴─────────────┴─────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  2. NARRATOLOGICAL-ALGORITHMS: Unifying story system       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing modular design, verify:

- [ ] Modules have clear single responsibilities
- [ ] Interfaces are well-defined
- [ ] Connections are typed/validated
- [ ] Feedback loops are controlled
- [ ] State is explicit
- [ ] Modules are independently testable
- [ ] System can evolve without rewrites
- [ ] Documentation explains the graph

## Common Scenarios

### Complex Generative System

1. **Modular Synthesis Philosophy:** Overall architecture
2. **Generative Art Algorithms:** Visual modules
3. **Generative Music Composer:** Audio modules
4. **Three.js Interactive Builder:** Integration layer

### Patchable Visual Tool

1. **Modular Synthesis Philosophy:** Patch paradigm
2. **Algorithmic Art:** Visual node implementations
3. **Canvas Design:** Output rendering

### Adaptive Audio-Visual Installation

1. **Modular Synthesis Philosophy:** System architecture
2. **Generative Music Composer:** Audio synthesis modules
3. **Three.js Interactive Builder:** Visual modules
4. **Narratological Algorithms:** State management

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| God modules | Too much responsibility | Split into focused modules |
| Spaghetti connections | Unmaintainable | Clear routing conventions |
| Implicit state | Hard to debug | Explicit state management |
| Over-modularization | Too complex | Find right granularity |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
