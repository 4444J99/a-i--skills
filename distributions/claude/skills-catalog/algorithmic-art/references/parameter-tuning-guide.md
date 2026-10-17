# Parameter Tuning Guide

How to tune generative art parameters for gallery-quality output.

## The Tuning Process

### 1. Establish Baselines

Start with default values that produce recognizable output:

```javascript
// Flow field baseline
let params = {
  noiseScale: 0.005,    // Moderate variation
  particleCount: 5000,  // Visible trails
  stepSize: 2,          // Balanced movement
  lineWeight: 0.5,      // Subtle lines
  opacity: 10           // Accumulation visible
};
```

### 2. Identify Key Parameters

Every algorithm has 2-3 parameters that most affect output:

| Algorithm | Primary Parameter | Secondary Parameter |
|-----------|-------------------|---------------------|
| Flow fields | noiseScale | particleCount |
| Particle systems | force strength | lifespan |
| L-systems | angle | iterations |
| Fractals | iteration limit | escape radius |
| Cellular automata | rule set | initial density |

### 3. Sweep Ranges

Test parameter extremes to understand effect:

```
noiseScale: 0.001 (very smooth) → 0.1 (very turbulent)
           0.001   0.005   0.01   0.05   0.1
             │       │       │       │     │
          smooth   natural  active  chaotic noise
```

### 4. Find Sweet Spots

The best values usually aren't at extremes:

| Parameter | Too Low | Sweet Spot | Too High |
|-----------|---------|------------|----------|
| noiseScale | Boring, uniform | Organic, varied | Noisy, chaotic |
| particleCount | Sparse, empty | Rich, dense | Slow, cluttered |
| opacity | Invisible trails | Visible accumulation | Solid blobs |
| lineWeight | Invisible | Delicate/bold | Crude |

## Parameter Relationships

### Coupled Parameters

Some parameters must change together:

```javascript
// If you increase particles, decrease opacity
particleCount: 10000 → opacity: 5
particleCount: 1000  → opacity: 25

// If you increase noise scale, decrease step size
noiseScale: 0.01 → stepSize: 1
noiseScale: 0.001 → stepSize: 4
```

### Ratio Relationships

```javascript
// Canvas size to particle count
particleCount = width * height / 50;

// Noise scale to canvas size
noiseScale = 5 / Math.max(width, height);
```

## Common Fixes

### Problem: Output looks random/chaotic
- Decrease noise scale
- Increase smoothing/interpolation
- Add constraints (boundaries, forces)

### Problem: Output looks too uniform
- Increase noise scale
- Add layered noise octaves
- Introduce random variation

### Problem: Lines too faint
- Increase line weight
- Increase opacity
- Decrease particle count (fewer, more visible)

### Problem: Performance issues
- Decrease particle count
- Increase step size (fewer calculations)
- Reduce canvas resolution

### Problem: Patterns don't fill space
- Increase particle lifespan
- Change edge behavior (wrap vs bounce)
- Add more seed points

## Seed Evaluation

### What makes a good seed?

Test seeds 1-100 and categorize:

| Category | Characteristics | Keep? |
|----------|-----------------|-------|
| Showcase | Balanced, striking, unique | Yes - feature |
| Solid | Good composition, typical | Yes - gallery |
| Weak | Unbalanced, sparse, dull | No |
| Interesting | Unusual but compelling | Yes - variety |

### Seed Documentation

```javascript
// Document exceptional seeds
const notableSeeds = {
  12: "Perfect spiral balance",
  47: "Unusual density pattern",
  73: "Best color distribution",
  91: "Edge case - sparse but elegant"
};
```

## Final Polish Checklist

- [ ] Parameters produce consistent quality across seeds
- [ ] No obvious artifacts or glitches
- [ ] Colors harmonious and intentional
- [ ] Composition balanced (visual weight distributed)
- [ ] Performance acceptable (smooth animation if applicable)
- [ ] Edge cases handled (boundaries, extremes)
- [ ] Reproducible (same seed = same output)
