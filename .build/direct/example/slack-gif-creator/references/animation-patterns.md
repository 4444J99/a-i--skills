# Animation Patterns Guide

Common animation patterns and their implementations for Slack GIFs.

## Core Animation Principles

### The 12 Principles (Adapted for GIFs)

| Principle | Application for GIFs |
|-----------|---------------------|
| Squash & Stretch | Exaggerate impact moments |
| Anticipation | Small wind-up before main action |
| Staging | Clear focal point, simple background |
| Follow Through | Objects settle after motion |
| Slow In/Out | Ease transitions, don't start/stop abruptly |
| Arcs | Natural motion follows curves |
| Secondary Action | Small details enhance main action |
| Timing | More frames = slower, fewer = snappier |
| Exaggeration | Push emotions and reactions |
| Solid Drawing | Keep proportions consistent |
| Appeal | Make it fun to watch |

---

## Reaction GIF Patterns

### The Classic Shake

**Use for:** Shock, fear, anger, excitement

```
Pattern:
1. Static hold (5 frames)
2. Quick shake sequence (15-20 frames)
3. Gradual settle (5 frames)

Shake motion:
- Horizontal: ±10-15px per frame
- Vertical: ±5-8px per frame
- Random variation prevents robotic feel
```

**Frame breakdown:**
```
Frame 1-5:   Center position (build tension)
Frame 6:    +12px right
Frame 7:    -10px left
Frame 8:    +8px right
Frame 9:    -12px left
...continue with decreasing amplitude...
Frame 20-25: Settle back to center
```

### The Bounce

**Use for:** Energy, enthusiasm, approval

```
Pattern:
1. Drop phase (accelerating down)
2. Impact squash
3. Rise phase (decelerating up)
4. Settle bounces (diminishing)

Easing:
- Down: ease_in (accelerate)
- Up: ease_out (decelerate)
- Squash: 80% height, 120% width at impact
```

### The Pulse/Heartbeat

**Use for:** Love, importance, attention

```
Pattern (heartbeat):
1. Quick expansion (3 frames)
2. Quick contraction (3 frames)
3. Quick expansion (3 frames)
4. Slow contraction (6 frames)
5. Pause (5 frames)
6. Repeat

Scale values:
- Rest: 100%
- First beat: 115%
- Second beat: 120%
```

### The Spin

**Use for:** Loading, confusion, celebration

```
Pattern:
- Full rotation over N frames
- Ease in/out for natural feel
- Consider rotation direction for meaning

Rotation per frame:
rotation = 360 * (frame / total_frames)

With easing:
rotation = 360 * ease_in_out(frame / total_frames)
```

---

## Impact Patterns

### The Slam

**Use for:** Emphasis, power, arrival

```
Pattern:
1. Object enters from off-screen (fast)
2. Impact frame (scale up, flash)
3. Screen shake (3-5 frames)
4. Settle

Timeline:
Frames 1-8:   Object moving in (ease_in)
Frame 9:      Impact + flash
Frames 10-15: Screen shake
Frames 16-20: Settle
```

### The Explosion

**Use for:** Mind-blown, surprise, celebration

```
Pattern:
1. Build-up (optional pulse)
2. Burst frame (white flash)
3. Particles fly outward
4. Fade/settle

Particle behavior:
- Start at center
- Move outward with random angles
- Decelerate (ease_out)
- Optionally fade out
```

### The Pop-In

**Use for:** Appearance, notification, ta-da

```
Pattern:
1. Object at 0% scale (invisible)
2. Quick scale up to 110-120%
3. Bounce back to 100%

Timing:
- Scale up: 4-6 frames
- Overshoot: 2 frames
- Settle: 3-4 frames

Easing: elastic_out
```

---

## Looping Patterns

### Seamless Loop

**Key principle:** Last frame connects smoothly to first frame

```
Types:
1. Boomerang: Action forward, then reverse
2. Continuous: End position = start position
3. Crossfade: Last frames fade into first frames

Boomerang structure:
Frames 1-15: Forward motion
Frames 16-30: Exact reverse of 1-15
```

### Idle Animation

**Use for:** Waiting states, subtle life

```
Pattern:
- Subtle bobbing (sine wave motion)
- Blink cycle for characters
- Gentle rotation or sway

Bobbing formula:
y_offset = amplitude * sin(frame * frequency)

Typical values:
- amplitude: 3-8 pixels
- frequency: 0.2-0.4
```

---

## Transition Patterns

### Slide In/Out

**Use for:** Entry/exit, scene changes

```
Direction options:
- Left, Right, Top, Bottom
- Diagonal

Pattern (slide in):
1. Start off-screen
2. Move to final position with easing
3. Optional overshoot + settle

Off-screen positions:
- From left: x = -object_width
- From right: x = canvas_width
- From top: y = -object_height
- From bottom: y = canvas_height
```

### Fade In/Out

**Use for:** Subtle transitions, text reveal

```
Pattern:
- Adjust alpha from 0 to 255 (or reverse)
- Linear or eased

For GIF (no true alpha):
- Simulate with dithering
- Or: scale from 0 with crossfade effect
```

### Morph/Transform

**Use for:** Before/after, reactions, surprises

```
Pattern:
1. Object A visible
2. Transition (scale, spin, fade)
3. Object B visible

Techniques:
- Crossfade: A fades out while B fades in
- Scale: A shrinks while B grows
- Flip: 3D rotation effect
```

---

## Emoji-Specific Patterns

### Size Constraints

For 128x128 emoji GIFs under 64KB:

```
Optimization priority:
1. Fewer frames (10-15 max)
2. Fewer colors (32-48)
3. Simple motion
4. Solid colors over gradients
5. Smaller emoji size (60-80px in frame)
```

### Effective Emoji Animations

| Animation | Frames | Colors | Typical Size |
|-----------|--------|--------|--------------|
| Simple pulse | 10-12 | 32 | 20-40KB |
| Quick shake | 12-15 | 32 | 25-45KB |
| Bounce once | 12-15 | 40 | 30-50KB |
| Spin | 15-20 | 32 | 35-55KB |

### Emoji Do's and Don'ts

**Do:**
- Single focal point
- Clear, simple motion
- High contrast
- Test at actual emoji size

**Don't:**
- Multiple moving elements
- Gradients or shadows
- Tiny text
- Complex backgrounds

---

## Timing Reference

### Frame Duration Guide

| Feel | FPS | Frame Duration |
|------|-----|----------------|
| Snappy/Energetic | 20-24 | 40-50ms |
| Normal | 15-18 | 55-65ms |
| Smooth | 12-15 | 65-85ms |
| Slow/Dreamy | 8-10 | 100-125ms |

### Motion Duration Reference

| Action | Frames @ 15fps | Seconds |
|--------|----------------|---------|
| Quick reaction | 5-8 | 0.3-0.5s |
| Normal action | 10-15 | 0.6-1.0s |
| Emphasis | 15-25 | 1.0-1.6s |
| Full sequence | 30-60 | 2.0-4.0s |

---

## Composing Complex Animations

### Layered Approach

```
Background layer: Static or subtle
Main action layer: Primary animation
Foreground layer: Effects, particles
Text layer: Labels, reactions

Render order:
1. Draw background
2. Draw main elements
3. Draw effects
4. Draw text
```

### Sequenced Actions

```
Act 1: Setup (anticipation)
Act 2: Action (main event)
Act 3: Reaction (follow-through)

Example - "Mind Blown":
Act 1: Head tilts, eyes widen (8 frames)
Act 2: Explosion effect (5 frames)
Act 3: Stars/particles settle (12 frames)
```

### Parallel Motion

```
Multiple elements moving simultaneously:
- Stagger start times for visual interest
- Vary speeds slightly
- Keep one element as focal point

Example - Celebration:
- Emoji bounces (main action)
- Confetti falls (secondary, offset start)
- Background pulses (tertiary, subtle)
```

---

## Quick Reference Card

### Common Easing Uses

| Motion | Easing |
|--------|--------|
| Object falling | ease_in |
| Object landing | bounce_out |
| Object appearing | elastic_out |
| Object disappearing | ease_in |
| Object moving through | ease_in_out |
| Impact | linear (fast) |

### Size Targets

| Type | Dimensions | Max Size |
|------|------------|----------|
| Message GIF | 480x480 | 2MB |
| Small emoji | 128x128 | 64KB |
| Reaction | 320x320 | 1MB |

### Loop Points

| Animation | Good Loop Length |
|-----------|------------------|
| Pulse | 20-30 frames |
| Shake | 20-25 frames |
| Bounce | 25-40 frames |
| Idle | 30-60 frames |
