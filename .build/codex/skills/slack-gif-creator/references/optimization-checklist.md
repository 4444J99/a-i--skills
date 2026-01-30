# GIF Optimization Checklist

Strategies to meet Slack's size requirements.

## Size Limits Quick Reference

| Type | Max Size | Dimensions | Target FPS |
|------|----------|------------|------------|
| Message GIF | 2 MB | 480x480 | 15-20 |
| Emoji GIF | 64 KB | 128x128 | 10-12 |
| Custom reaction | 1 MB | 320x320 | 12-15 |

---

## Optimization Checklist

### Before Creating

- [ ] Identify target use (emoji vs message)
- [ ] Plan simple design (fewer elements = smaller size)
- [ ] Choose limited color palette upfront
- [ ] Estimate frame count based on size target

### During Creation

- [ ] Use solid colors over gradients
- [ ] Minimize moving elements
- [ ] Avoid complex backgrounds
- [ ] Keep text large and readable
- [ ] Check frame count periodically

### After Creating

- [ ] Validate file size against target
- [ ] Reduce colors if over size
- [ ] Remove redundant frames
- [ ] Test visual quality at actual display size
- [ ] Verify loop is seamless

---

## Size Reduction Techniques

### 1. Reduce Colors

**Impact:** High
**Quality Loss:** Low-Medium

| Colors | Typical Size Reduction | Quality |
|--------|----------------------|---------|
| 256 → 128 | 15-25% | Minimal loss |
| 128 → 64 | 20-30% | Some banding |
| 64 → 32 | 25-35% | Noticeable |
| 32 → 16 | 30-40% | Significant |

**Best for:**
- Simple graphics
- Flat colors
- Icons and emojis

**Avoid when:**
- Photographic content
- Subtle gradients needed
- Complex shading

### 2. Reduce Frame Count

**Impact:** High
**Quality Loss:** Medium

| Change | Size Reduction | Effect |
|--------|---------------|--------|
| 24fps → 15fps | ~35% | Slightly choppy |
| 15fps → 10fps | ~30% | Noticeable |
| 30 → 20 frames | ~33% | Shorter duration |

**Strategies:**
- Remove every other frame (halves size)
- Shorten animation duration
- Combine similar frames

### 3. Reduce Dimensions

**Impact:** Very High
**Quality Loss:** Low (if appropriate for use)

| Change | Size Reduction |
|--------|---------------|
| 480 → 320 | ~55% |
| 320 → 256 | ~35% |
| 256 → 128 | ~75% |

**When to use:**
- Always for emoji GIFs (128px)
- When GIF will be displayed small
- As last resort for message GIFs

### 4. Optimize Frame Content

**Impact:** Medium
**Quality Loss:** None

| Technique | Description |
|-----------|-------------|
| Static backgrounds | Don't redraw unchanged areas |
| Smaller motion range | Less pixel change = smaller |
| Solid colors | Compress better than patterns |
| Limited palette | Use same colors throughout |

### 5. Enable Frame Disposal

**Impact:** Medium
**Quality Loss:** None

```
Frame disposal methods:
- Keep: Keep previous frame (for partial updates)
- Restore to background: Clear before next frame
- Restore to previous: Return to prior state

Use for:
- Small moving objects on static background
- Overlay effects
- Text animations
```

---

## Emoji GIF Strategy (64KB Limit)

The 64KB limit is the hardest to meet. Follow this order:

### Step 1: Aggressive Settings

```
Dimensions: 128x128 (required)
Colors: 32 maximum
Frames: 10-15 maximum
FPS: 10
Duration: 1-1.5 seconds
```

### Step 2: Design Constraints

| Do | Don't |
|----|-------|
| Single emoji/element | Multiple moving elements |
| Solid background | Gradients |
| Simple motion | Complex paths |
| 1 color background | Textured backgrounds |
| Bold, simple | Detailed, subtle |

### Step 3: Animation Selection

**Safe animations (fit in 64KB):**
- Simple pulse (10 frames, 32 colors)
- Quick shake (12 frames, 32 colors)
- Single bounce (12 frames, 40 colors)
- Slow spin (15 frames, 32 colors)

**Risky animations (may exceed):**
- Multiple bounces
- Complex easing
- Color changes
- Particle effects

### Step 4: Iterative Reduction

```
If over 64KB:
1. Reduce to 10 frames
2. Reduce to 24 colors
3. Simplify animation
4. Remove any effects
5. Try different animation type
```

---

## Message GIF Strategy (2MB Limit)

More flexibility, but still optimize for faster loading.

### Recommended Settings

```
Dimensions: 480x480 (or smaller)
Colors: 128-256
Frames: 30-60
FPS: 15-20
Duration: 2-4 seconds
```

### When Approaching Limit

| Current Size | Action |
|--------------|--------|
| 1.5-2 MB | Reduce colors to 128 |
| 2-2.5 MB | Reduce colors to 64, cut frames |
| 2.5+ MB | Reduce dimensions to 320 |

---

## Quality vs Size Trade-offs

### Visual Priority Matrix

| If you need... | Sacrifice... |
|----------------|--------------|
| Smooth motion | Colors, dimensions |
| Rich colors | Frame rate, duration |
| Large display | Frame count, colors |
| Long duration | FPS, colors, dimensions |

### Minimum Quality Standards

| Element | Minimum Acceptable |
|---------|-------------------|
| Emoji/Icon | 32 colors, 10fps |
| Character animation | 64 colors, 12fps |
| Text animation | 48 colors, 10fps |
| Scene animation | 128 colors, 15fps |

---

## Validation Checklist

### Before Upload

- [ ] File size under limit
  - Emoji: < 64 KB
  - Message: < 2 MB
- [ ] Dimensions correct
  - Emoji: 128x128
  - Message: 480x480 or smaller
- [ ] Loop looks seamless
- [ ] Animation timing feels right
- [ ] Text readable (if present)
- [ ] Works at actual display size

### Testing

1. **View at actual size** - Not zoomed in editor
2. **Test in Slack** - Upload to test channel
3. **Check on mobile** - May render differently
4. **Verify loop** - Watch multiple times

---

## Optimization Tools

### Python/PIL Workflow

```python
# After creating GIF, check and optimize

import os

# Check size
size_kb = os.path.getsize('output.gif') / 1024
print(f"Size: {size_kb:.1f} KB")

# If over limit, try:
# 1. Reduce colors in save()
# 2. Remove frames
# 3. Resize dimensions
```

### Command Line (ImageMagick/Gifsicle)

```bash
# Check file size
ls -lh output.gif

# Optimize with gifsicle
gifsicle -O3 --colors 64 output.gif -o optimized.gif

# Resize with ImageMagick
convert output.gif -resize 128x128 emoji.gif
```

### Quick Size Estimation

```
Rough estimate (uncompressed):
Size ≈ Width × Height × Frames × (Colors/256) × 0.3

Example:
128 × 128 × 15 × (32/256) × 0.3 = ~9 KB (before optimization)

Actual will vary based on content complexity.
```

---

## Troubleshooting

### "File too large" after optimization

1. Already at minimum colors (32)?
   → Reduce frames
2. Already at minimum frames (10)?
   → Simplify animation type
3. Already simple animation?
   → Consider different approach

### "Animation looks choppy"

- Below 10fps will look choppy
- Consider fewer frames with same duration
- Use easing to improve perceived smoothness

### "Colors look wrong"

- GIF uses palette, not true color
- Avoid gradients
- Test with target color count early
- Consider dithering for better gradients

### "Loop has a jump"

- Ensure first and last frames align
- Use boomerang pattern for guaranteed smooth
- Check frame disposal settings
