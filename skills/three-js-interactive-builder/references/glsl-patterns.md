# GLSL Shader Patterns

## Glow/Bloom Effect

```glsl
// Fragment shader for soft glow
uniform float glowIntensity;
uniform vec3 glowColor;

void main() {
  float dist = length(vUv - 0.5) * 2.0;
  float glow = 1.0 - smoothstep(0.0, 1.0, dist);
  glow = pow(glow, 2.0) * glowIntensity;
  gl_FragColor = vec4(glowColor * glow, glow);
}
```

## Simplex Noise 2D

```glsl
vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }

float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
  m = m*m; m = m*m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
  vec3 g;
  g.x = a0.x * x0.x + h.x * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
```

## Gradient Color Mapping

```glsl
// Map value to gradient (0-1 input)
vec3 gradient(float t, vec3 color1, vec3 color2, vec3 color3) {
  return t < 0.5 
    ? mix(color1, color2, t * 2.0) 
    : mix(color2, color3, (t - 0.5) * 2.0);
}

// Chakra-inspired 7-color gradient
vec3 chakraGradient(float t) {
  vec3 colors[7];
  colors[0] = vec3(0.8, 0.2, 0.2); // Root - Red
  colors[1] = vec3(1.0, 0.5, 0.2); // Sacral - Orange
  colors[2] = vec3(1.0, 0.9, 0.3); // Solar - Yellow
  colors[3] = vec3(0.3, 0.8, 0.4); // Heart - Green
  colors[4] = vec3(0.3, 0.6, 0.9); // Throat - Blue
  colors[5] = vec3(0.4, 0.3, 0.8); // Third Eye - Indigo
  colors[6] = vec3(0.7, 0.4, 0.9); // Crown - Violet
  
  float segment = t * 6.0;
  int idx = int(floor(segment));
  float frac = fract(segment);
  return mix(colors[idx], colors[min(idx + 1, 6)], frac);
}
```

## Polar Coordinates

```glsl
// Convert UV to polar
vec2 toPolar(vec2 uv) {
  vec2 centered = uv - 0.5;
  float r = length(centered) * 2.0;
  float theta = atan(centered.y, centered.x);
  return vec2(r, theta);
}

// Spiral pattern
float spiral(vec2 uv, float arms, float twist) {
  vec2 polar = toPolar(uv);
  return sin(polar.y * arms + polar.x * twist);
}
```

## Sacred Symbol Masks

```glsl
// Vesica Piscis
float vesicaPiscis(vec2 uv, float offset) {
  float d1 = length(uv - vec2(-offset, 0.0));
  float d2 = length(uv - vec2(offset, 0.0));
  float r = offset * 2.0;
  return step(d1, r) * step(d2, r);
}

// Six-pointed star (Star of David)
float hexagram(vec2 uv, float size) {
  vec2 p = abs(uv);
  float tri1 = max(p.x * 0.866 + p.y * 0.5, p.y) - size;
  vec2 q = vec2(p.x, -uv.y);
  float tri2 = max(q.x * 0.866 + q.y * 0.5, q.y) - size;
  return min(step(tri1, 0.0), step(tri2, 0.0));
}
```

## Animated Effects

```glsl
// Pulsing glow
float pulse(float t, float speed, float min, float max) {
  return min + (max - min) * (0.5 + 0.5 * sin(t * speed));
}

// Rotating pattern
vec2 rotate(vec2 uv, float angle) {
  float c = cos(angle);
  float s = sin(angle);
  return vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);
}
```
