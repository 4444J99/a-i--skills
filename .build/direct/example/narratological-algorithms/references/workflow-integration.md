# Workflow Integration: Narratological Algorithms

This document describes how `narratological-algorithms` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `three-js-interactive-builder` | **Downstream** | Interactive narrative experiences |
| `generative-music-composer` | **Complementary** | Story-driven music progression |
| `modular-synthesis-philosophy` | **Complementary** | Story as modular system |
| `canvas-design` | **Complementary** | Visual narrative design |
| `algorithmic-art` | **Complementary** | Story-reactive visuals |

## Prerequisites

Before invoking `narratological-algorithms`, ensure:

1. **Story concept exists** - Core narrative to formalize
2. **Medium determined** - Interactive, linear, generative
3. **Audience known** - Who experiences the narrative

## Handoff Patterns

### To: three-js-interactive-builder

**Trigger:** Narrative needs interactive implementation.

**What to hand off:**
- Story state machine
- Beat definitions and triggers
- Progression requirements
- Character/entity specifications

**Expected output from three-js:**
- Interactive story environment
- State-based scene changes
- User choice implementations

### To: generative-music-composer

**Trigger:** Music should follow narrative arc.

**What to hand off:**
- Emotional arc map
- Story state definitions
- Pacing requirements
- Tension/release points

**Expected output from composer:**
- Adaptive score system
- State-triggered music changes
- Leitmotif implementations

### From: modular-synthesis-philosophy

**Trigger:** Story designed as modular system.

**What to receive:**
- Modular component thinking
- State machine patterns
- Recombination strategies

**Integration points:**
- Story beats as modules
- Composable narrative elements
- Branching/recombination logic

### To: canvas-design

**Trigger:** Visualize narrative structure.

**What to hand off:**
- Story structure diagram
- Beat hierarchy
- Pacing visualization

**Expected output from canvas:**
- Story structure infographic
- Visual timeline
- Character relationship map

### To: algorithmic-art

**Trigger:** Visuals respond to narrative state.

**What to hand off:**
- Story states and parameters
- Emotional values
- Transition events

**Expected output from algorithmic:**
- State-reactive visuals
- Mood-based generation
- Narrative-driven patterns

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Narrative System Design                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MODULAR-SYNTHESIS-PHILOSOPHY: System approach          │
│           │                                                 │
│           ▼                                                 │
│  2. NARRATOLOGICAL-ALGORITHMS: Formalize story structure   │
│           │                                                 │
│           ├─────────────────────────────────────────┐       │
│           │             │             │             │       │
│           ▼             ▼             ▼             ▼       │
│      THREE-JS       GEN-MUSIC    ALGORITHMIC     CANVAS    │
│      BUILDER        COMPOSER        ART          DESIGN    │
│      (interact)     (score)       (visuals)      (docs)    │
│           │             │             │             │       │
│           └─────────────┴─────────────┴─────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing narrative algorithm, verify:

- [ ] Story structure is coherent
- [ ] All paths lead to meaningful outcomes
- [ ] Beats are well-defined
- [ ] State transitions are clear
- [ ] Pacing is appropriate
- [ ] Character arcs are complete
- [ ] Theme is consistently expressed
- [ ] Edge cases handled (stuck states)

## Common Scenarios

### Interactive Fiction

1. **Narratological Algorithms:** Story graph structure
2. **Three.js Interactive Builder:** Interactive environment
3. **Generative Music Composer:** Adaptive soundtrack

### Generative Storytelling

1. **Modular Synthesis Philosophy:** Modular story approach
2. **Narratological Algorithms:** Recombinatorial narrative
3. **Algorithmic Art:** Story-driven visuals

### Experience Design

1. **Narratological Algorithms:** Experience arc
2. **Generative Music Composer:** Emotional score
3. **Three.js Interactive Builder:** Immersive environment

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Dead ends | Stuck players | Always provide exit paths |
| Inconsistent tone | Broken immersion | Define tone guidelines |
| Obvious branching | Breaks engagement | Subtle choice consequences |
| No payoff | Unsatisfying experience | Ensure meaningful conclusions |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
