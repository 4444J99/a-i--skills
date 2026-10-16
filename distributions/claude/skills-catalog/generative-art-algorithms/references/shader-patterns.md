# Shader Patterns

GLSL fragment shader snippets for generative art. These patterns run on the GPU and can be used in Shadertoy, GLSL Sandbox, Three.js, or any WebGL context.

## Shader Fundamentals

### Minimal Fragment Shader

```glsl
// Shadertoy-compatible: fragCoord is pixel position, iResolution is canvas size
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;  // Normalize to 0-1
    fragColor = vec4(uv.x, uv.y, 0.0, 1.0);
}
```

### Common Uniforms

| Uniform | Type | Description |
|---------|------|-------------|
| `iResolution` | `vec3` | Canvas width, height, pixel ratio |
| `iTime` | `float` | Seconds since start |
| `iMouse` | `vec4` | Mouse position (xy: current, zw: click) |
| `iFrame` | `int` | Frame number |

### Coordinate Systems

```glsl
vec2 uv = fragCoord / iResolution.xy;                          // Normalized 0-1
vec2 uv = (fragCoord * 2.0 - iResolution.xy) / iResolution.y;  // Centered -1 to 1
vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.y;  // Aspect-corrected
```

---

## Distance Functions (2D SDF)

```glsl
float sdCircle(vec2 p, float r) {
    return length(p) - r;
}

float sdBox(vec2 p, vec2 b) {
    vec2 d = abs(p) - b;
    return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

float sdSegment(vec2 p, vec2 a, vec2 b) {
    vec2 pa = p - a, ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h);
}
```

### SDF Operations

```glsl
float opUnion(float d1, float d2) { return min(d1, d2); }
float opSubtract(float d1, float d2) { return max(-d1, d2); }
float opIntersect(float d1, float d2) { return max(d1, d2); }

// Smooth union (organic blending)
float opSmoothUnion(float d1, float d2, float k) {
    float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return mix(d2, d1, h) - k * h * (1.0 - h);
}
```

---

## Noise in GLSL

### Hash and Value Noise

```glsl
float hash(vec2 p) {
    p = fract(p * vec2(123.34, 456.21));
    p += dot(p, p + 45.32);
    return fract(p.x * p.y);
}

float valueNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);  // Smoothstep interpolation
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
    float value = 0.0, amplitude = 0.5;
    for (int i = 0; i < 6; i++) {
        value += amplitude * valueNoise(p);
        p *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
```

---

## Generative Patterns

### Voronoi Cells

```glsl
float voronoi(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float minDist = 1.0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec2 neighbor = vec2(float(x), float(y));
            vec2 point = vec2(hash(i + neighbor), hash(i + neighbor + 100.0));
            point = 0.5 + 0.5 * sin(iTime + 6.2831 * point);  // Animate
            minDist = min(minDist, length(neighbor + point - f));
        }
    }
    return minDist;
}
```

### Truchet Tiles

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.y;
    float scale = 10.0;
    vec2 cell = floor(uv * scale);
    vec2 f = fract(uv * scale);
    if (step(0.5, hash(cell)) > 0.5) f.x = 1.0 - f.x;
    float d = min(abs(length(f) - 0.5), abs(length(f - 1.0) - 0.5));
    fragColor = vec4(vec3(smoothstep(0.05, 0.03, d)), 1.0);
}
```

---

## Color Techniques

### Cosine Palette (Inigo Quilez)

```glsl
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    return a + b * cos(6.28318 * (c * t + d));
}
// Rainbow:  palette(t, vec3(0.5), vec3(0.5), vec3(1.0), vec3(0.0, 0.33, 0.67))
// Sunset:   palette(t, vec3(0.5), vec3(0.5), vec3(1.0,0.7,0.4), vec3(0.0,0.15,0.2))
// Ice:      palette(t, vec3(0.5,0.5,0.7), vec3(0.2,0.3,0.5), vec3(1.0), vec3(0.0,0.1,0.2))
```

---

## Domain Manipulation

### Repetition and Polar Coordinates

```glsl
// Infinite tiling
vec2 repeat(vec2 p, float spacing) {
    return mod(p + spacing * 0.5, spacing) - spacing * 0.5;
}

// Polar conversion
vec2 toPolar(vec2 p) {
    return vec2(length(p), atan(p.y, p.x));
}

// Kaleidoscope
float kaleidoscope(vec2 p, float segments) {
    float angle = atan(p.y, p.x);
    float segAngle = 6.28318 / segments;
    angle = mod(angle, segAngle);
    return abs(angle - segAngle * 0.5);
}
```

### Domain Warping

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec2 q = vec2(fbm(uv + iTime * 0.1), fbm(uv + vec2(5.2, 1.3)));
    vec2 r = vec2(fbm(uv + 4.0 * q + vec2(1.7, 9.2) + 0.15 * iTime),
                  fbm(uv + 4.0 * q + vec2(8.3, 2.8) + 0.126 * iTime));
    float f = fbm(uv + 4.0 * r);
    fragColor = vec4(mix(vec3(0.1, 0.05, 0.2), vec3(0.9, 0.4, 0.1), f), 1.0);
}
```

---

## Useful Math

```glsl
// Remap value from one range to another
float remap(float value, float inMin, float inMax, float outMin, float outMax) {
    return outMin + (value - inMin) * (outMax - outMin) / (inMax - inMin);
}

// Rotation matrix
mat2 rot(float a) {
    float s = sin(a), c = cos(a);
    return mat2(c, -s, s, c);
}
```

## Performance Tips

| Technique | Purpose |
|-----------|---------|
| Use `smoothstep` over `if` | Avoids GPU branch divergence |
| Minimize texture lookups | Each lookup has latency |
| Pre-compute constants outside loops | Avoid redundant math |
| Lower `fbm` octaves for previewing | 3-4 while developing, 6-8 for final |
| Use `fract` and `mod` for tiling | Cheaper than conditional wrapping |
