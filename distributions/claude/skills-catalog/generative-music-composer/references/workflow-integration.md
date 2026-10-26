# Workflow Integration: Generative Music Composer

This document describes how `generative-music-composer` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `modular-synthesis-philosophy` | **Upstream** | Receive system design approach |
| `narratological-algorithms` | **Complementary** | Story-driven music progression |
| `three-js-interactive-builder` | **Complementary** | Audio-visual synchronization |
| `algorithmic-art` | **Complementary** | Music-reactive visuals |
| `generative-art-algorithms` | **Complementary** | Algorithmic composition |

## Prerequisites

Before invoking `generative-music-composer`, ensure:

1. **Musical concept defined** - Genre, mood, instrumentation
2. **Generation approach chosen** - Rule-based, stochastic, ML
3. **Platform requirements known** - Web Audio, native, DAW

## Handoff Patterns

### From: modular-synthesis-philosophy

**Trigger:** Design generative audio system architecture.

**What to receive:**
- Signal flow concepts
- Modular architecture patterns
- Patch-based thinking

**Integration points:**
- Design audio module graph
- Implement parameter patching
- Create feedback systems

### To: three-js-interactive-builder

**Trigger:** Visuals need audio synchronization.

**What to hand off:**
- Beat detection callbacks
- Frequency analysis data
- Musical structure events

**Expected output from three-js:**
- Audio-reactive visual elements
- Synchronized animations
- Musical event responses

### To: algorithmic-art

**Trigger:** Create music-reactive visuals.

**What to hand off:**
- Audio analysis streams
- Musical parameter values
- Timing and tempo data

**Expected output from algorithmic:**
- Audio-reactive pattern system
- Parameter mappings
- Visual-audio coherence

### From/To: narratological-algorithms

**Trigger:** Music follows or drives narrative.

**What to exchange:**
- Story state machine (from narrative)
- Emotional arc (from narrative)
- Musical cues (to narrative)
- Pacing signals (to narrative)

**Integration points:**
- Adaptive music for story states
- Leitmotifs for narrative elements
- Tension/release aligned with story

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Generative Music Creation                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MODULAR-SYNTHESIS-PHILOSOPHY: System architecture      │
│           │                                                 │
│           ▼                                                 │
│  2. GENERATIVE-MUSIC-COMPOSER: Create music system         │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. THREE-JS-BUILDER          3b. ALGORITHMIC-ART         │
│      (visual sync)                 (reactive visuals)      │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. NARRATOLOGICAL-ALGORITHMS: Story integration           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing generative music, verify:

- [ ] Musical output is coherent
- [ ] Transitions are smooth
- [ ] Tempo and key are consistent
- [ ] Web Audio API correctly initialized
- [ ] Audio context resumes on user interaction
- [ ] Memory managed (no audio buffer leaks)
- [ ] Volume and dynamics controlled
- [ ] Export capability (if needed)

## Common Scenarios

### Adaptive Game Music

1. **Modular Synthesis Philosophy:** Stem-based architecture
2. **Generative Music Composer:** Layered adaptive system
3. **Narratological Algorithms:** Game state integration

### Audio-Visual Performance

1. **Generative Music Composer:** Live generative music
2. **Three.js Interactive Builder:** Synchronized visuals
3. **Algorithmic Art:** Reactive patterns

### Ambient Generative Installation

1. **Modular Synthesis Philosophy:** Infinite generation design
2. **Generative Music Composer:** Long-form ambient system
3. **Generative Art Algorithms:** Slow evolution patterns

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No user gesture | Audio blocked | Wait for user interaction |
| Glitchy transitions | Jarring experience | Crossfade and schedule carefully |
| Monotonous output | Boring | Add variation and evolution |
| Memory leaks | Crashes over time | Properly dispose audio buffers |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
