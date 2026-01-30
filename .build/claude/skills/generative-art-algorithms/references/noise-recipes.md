# Noise Function Recipes

Practical patterns for using noise in generative art.

## Basic Noise Usage

### Single Layer (Simplex/Perlin)

```javascript
// Simple terrain-like values
let value = noise(x * scale, y * scale);
// Returns 0-1 in p5.js, use for height, color, etc.
```

### Animated Noise

```javascript
// Add time dimension for movement
let value = noise(x * scale, y * scale, frameCount * timeScale);
// timeScale: 0.001 = very slow, 0.01 = moderate, 0.1 = fast
```

## Fractal Brownian Motion (fBm)

Layering noise at different scales for natural complexity.

```javascript
function fbm(x, y, octaves, lacunarity, gain) {
  let value = 0;
  let amplitude = 1;
  let frequency = 1;
  let maxValue = 0;

  for (let i = 0; i < octaves; i++) {
    value += amplitude * noise(x * frequency, y * frequency);
    maxValue += amplitude;
    amplitude *= gain;      // Each octave contributes less
    frequency *= lacunarity; // Each octave is higher frequency
  }

  return value / maxValue; // Normalize to 0-1
}

// Typical values:
// octaves: 4-8
// lacunarity: 2.0 (doubles frequency each octave)
// gain (persistence): 0.5 (halves amplitude each octave)
```

### fBm Variations

| Name | lacunarity | gain | Character |
|------|------------|------|-----------|
| Standard fBm | 2.0 | 0.5 | Balanced, natural |
| Turbulent | 2.0 | 0.7 | More high-frequency detail |
| Smooth | 2.0 | 0.3 | Dominated by low frequencies |
| Billowy | 2.5 | 0.5 | Stretched features |

## Domain Warping

Distort the input coordinates for organic effects.

```javascript
function warpedNoise(x, y, warpScale, warpStrength) {
  // First noise layer warps the coordinates
  let warpX = noise(x * warpScale, y * warpScale) * warpStrength;
  let warpY = noise(x * warpScale + 100, y * warpScale + 100) * warpStrength;

  // Second noise layer uses warped coordinates
  return noise((x + warpX) * 0.01, (y + warpY) * 0.01);
}
```

### Multi-level Warping

```javascript
function deepWarp(x, y) {
  // Warp the warp for even more organic results
  let wx1 = noise(x * 0.01, y * 0.01) * 100;
  let wy1 = noise(x * 0.01 + 5, y * 0.01 + 5) * 100;

  let wx2 = noise((x + wx1) * 0.02, (y + wy1) * 0.02) * 50;
  let wy2 = noise((x + wx1) * 0.02 + 5, (y + wy1) * 0.02 + 5) * 50;

  return noise((x + wx2) * 0.03, (y + wy2) * 0.03);
}
```

## Ridged Noise

Sharp ridges like mountain ranges.

```javascript
function ridgedNoise(x, y) {
  let value = noise(x, y);
  value = abs(value - 0.5) * 2; // Fold around 0.5
  return 1 - value; // Invert so ridges are peaks
}

// Or with fBm for more detail:
function ridgedFbm(x, y, octaves) {
  let value = 0;
  let amplitude = 1;
  let frequency = 1;
  let weight = 1;

  for (let i = 0; i < octaves; i++) {
    let n = 1 - abs(noise(x * frequency, y * frequency) - 0.5) * 2;
    n *= n * weight;
    weight = constrain(n, 0, 1);
    value += n * amplitude;
    amplitude *= 0.5;
    frequency *= 2;
  }

  return value;
}
```

## Cellular/Worley Noise

Distance to nearest point creates cell-like patterns.

```javascript
function worleyNoise(x, y, cellSize) {
  let cellX = floor(x / cellSize);
  let cellY = floor(y / cellSize);
  let minDist = Infinity;

  // Check neighboring cells
  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      let nx = cellX + i;
      let ny = cellY + j;

      // Random point in this cell (seeded by cell position)
      randomSeed(nx * 1000 + ny);
      let px = (nx + random()) * cellSize;
      let py = (ny + random()) * cellSize;

      let d = dist(x, y, px, py);
      minDist = min(minDist, d);
    }
  }

  return minDist / cellSize; // Normalize
}
```

## Flow Fields from Noise

Convert noise to directional vectors.

```javascript
function noiseToAngle(x, y, scale) {
  return noise(x * scale, y * scale) * TWO_PI * 2;
}

function noiseToVector(x, y, scale) {
  let angle = noiseToAngle(x, y, scale);
  return createVector(cos(angle), sin(angle));
}

// Curl noise for divergence-free flow (no sinks/sources)
function curlNoise(x, y, scale, eps) {
  // Approximate partial derivatives
  let dx = (noise(x + eps, y) - noise(x - eps, y)) / (2 * eps);
  let dy = (noise(x, y + eps) - noise(x, y - eps)) / (2 * eps);

  // Curl: rotate gradient 90 degrees
  return createVector(dy, -dx);
}
```

## Noise Color Mapping

```javascript
// Simple gradient
function noiseToColor(n) {
  colorMode(HSB);
  return color(n * 360, 70, 90);
}

// Custom palette
function noiseToColorPalette(n, palette) {
  let index = floor(n * (palette.length - 1));
  let t = (n * (palette.length - 1)) % 1;
  return lerpColor(palette[index], palette[index + 1], t);
}

// Stepped/posterized
function noiseStepped(n, steps) {
  return floor(n * steps) / steps;
}
```

## Common Parameters by Effect

| Effect | Scale | Octaves | Lacunarity | Gain |
|--------|-------|---------|------------|------|
| Clouds | 0.005 | 6 | 2.0 | 0.5 |
| Terrain | 0.01 | 4 | 2.2 | 0.45 |
| Marble | 0.02 | 3 | 2.0 | 0.65 |
| Wood grain | 0.1 × x, 0.01 × y | 2 | 2.0 | 0.5 |
| Water ripples | 0.05 | 2 | 3.0 | 0.3 |
| Smoke | 0.003 | 8 | 2.0 | 0.6 |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Too uniform | Scale too large | Decrease scale |
| Too chaotic | Scale too small | Increase scale |
| Repeating patterns | Integer coordinates | Use float positions |
| Sharp edges | Not enough octaves | Add more octaves |
| Too soft | Too many octaves | Reduce octaves |
| Drifting slowly | Time scale too small | Increase time scale |
