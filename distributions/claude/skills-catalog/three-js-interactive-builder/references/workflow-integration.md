# Workflow Integration: Three.js Interactive Builder

This document describes how `three-js-interactive-builder` integrates with other skills in the Creative Coding & Generative Systems ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `generative-art-algorithms` | **Upstream** | Receive algorithms for 3D implementation |
| `algorithmic-art` | **Upstream** | Extend 2D patterns to 3D |
| `canvas-design` | **Upstream** | Apply composition rules in 3D |
| `generative-music-composer` | **Complementary** | Synchronized audio |
| `narratological-algorithms` | **Complementary** | Story-driven experiences |

## Prerequisites

Before invoking `three-js-interactive-builder`, ensure:

1. **Scene concept defined** - What the 3D experience should be
2. **Interaction model known** - How users engage
3. **Performance target set** - FPS, device requirements

## Handoff Patterns

### From: generative-art-algorithms

**Trigger:** Algorithm needs 3D visualization.

**What to receive:**
- Mathematical algorithm definitions
- Parameter ranges and mappings
- Performance characteristics

**Integration points:**
- Implement in shaders
- Create procedural geometry
- Design particle systems

### From: algorithmic-art

**Trigger:** 2D patterns extend to 3D.

**What to receive:**
- Pattern logic
- Visual language
- Interaction patterns

**Integration points:**
- Project patterns onto 3D surfaces
- Create volumetric versions
- Maintain visual coherence

### From: canvas-design

**Trigger:** Apply 2D composition in 3D.

**What to receive:**
- Color systems
- Composition principles
- Typography rules

**Integration points:**
- Camera framing
- Material systems
- Lighting design

### To: generative-music-composer

**Trigger:** Scene needs synchronized audio.

**What to hand off:**
- Scene state events
- Interaction callbacks
- Timing requirements

**Expected output from music:**
- Reactive audio system
- Event-triggered sounds
- Ambient generative music

### To: narratological-algorithms

**Trigger:** Add story progression to scene.

**What to hand off:**
- Scene state machine
- User progress tracking
- Transition points

**Expected output from narrative:**
- Story beat definitions
- State progression logic
- Narrative triggers

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    3D Experience Creation                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. UPSTREAM SKILLS: Provide algorithms and design         │
│           │                                                 │
│           ├─────────────────────┬─────────────────┐         │
│           ▼                     ▼                 ▼         │
│      GEN-ART-ALG           ALGORITHMIC-ART    CANVAS       │
│           │                     │                 │         │
│           └─────────────────────┴─────────────────┘         │
│                          │                                  │
│                          ▼                                  │
│  2. THREE-JS-INTERACTIVE-BUILDER: Build 3D experience      │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. GENERATIVE-MUSIC-COMPOSER  3b. NARRATOLOGICAL-ALG     │
│      (audio integration)            (story progression)    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing 3D build, verify:

- [ ] Performance meets target FPS
- [ ] Scene loads progressively
- [ ] Interactions feel responsive
- [ ] Lighting enhances visuals
- [ ] Camera controls are intuitive
- [ ] Mobile/touch support (if needed)
- [ ] WebXR support (if needed)
- [ ] Fallbacks for older browsers

## Common Scenarios

### Interactive Data Visualization

1. **Generative Art Algorithms:** Data mapping algorithms
2. **Three.js Interactive Builder:** 3D visualization
3. **Canvas Design:** Color and composition

### Immersive Installation

1. **Algorithmic Art:** Pattern concepts
2. **Three.js Interactive Builder:** Immersive environment
3. **Generative Music Composer:** Spatial audio
4. **Narratological Algorithms:** Guided experience

### WebXR Experience

1. **Three.js Interactive Builder:** VR/AR scene
2. **Generative Art Algorithms:** Procedural content
3. **Generative Music Composer:** Spatial audio

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Too many draw calls | Poor performance | Instancing, merge geometries |
| Unoptimized textures | Memory issues | Use proper formats, mipmaps |
| Blocking main thread | Janky interactions | Use workers for heavy computation |
| No LOD | Wasted resources | Level of detail for complex scenes |

## Related Resources

- [Creative Coding Skills Ecosystem Map](../../../docs/guides/creative-coding-skills-ecosystem.md)
