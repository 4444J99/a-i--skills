# Sacred Geometry Mathematical Foundations

## Core Ratios

**Golden Ratio (φ)**: `(1 + √5) / 2 ≈ 1.618033988749`
- Appears in spirals, pentagons, human proportions
- Fibonacci sequence approximates: F(n)/F(n-1) → φ

**Silver Ratio (δ)**: `1 + √2 ≈ 2.414213562373`
- Octagonal geometry, Pell numbers

**Pi (π)**: `3.141592653589793`
- Circle circumference, wave functions

## Flower of Life Construction

Central circle with 6 surrounding circles of equal radius, centers on the circumference:

```
For radius r, center at origin:
Circle centers at angles: 0°, 60°, 120°, 180°, 240°, 300°
Position: (r × cos(angle), r × sin(angle))
```

Extend to 19 circles for complete Flower of Life.

## Metatron's Cube

13 circles arranged as:
- 1 central
- 6 inner ring (radius r from center)
- 6 outer ring (radius 2r from center, offset 30°)

Connect all 13 centers with lines to reveal Platonic solids.

## Platonic Solids Vertex Coordinates

**Tetrahedron** (4 vertices):
```
(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)
```

**Cube/Hexahedron** (8 vertices):
```
(±1, ±1, ±1)
```

**Octahedron** (6 vertices):
```
(±1, 0, 0), (0, ±1, 0), (0, 0, ±1)
```

**Dodecahedron** (20 vertices):
```
(±1, ±1, ±1)
(0, ±1/φ, ±φ)
(±1/φ, ±φ, 0)
(±φ, 0, ±1/φ)
```

**Icosahedron** (12 vertices):
```
(0, ±1, ±φ)
(±1, ±φ, 0)
(±φ, 0, ±1)
```

## Spiral Equations

**Archimedean Spiral**: `r = a + bθ` (constant spacing)

**Logarithmic/Golden Spiral**: `r = ae^(bθ)` where `b = ln(φ)/(π/2)`

**Fibonacci Spiral**: Quarter circles with radii following Fibonacci sequence

## Sri Yantra Construction

9 interlocking triangles (4 upward, 5 downward) around central bindu point.

Triangle vertices calculated from concentric circles with specific ratios:
- Start from bindu
- Each triangle layer uses precise angle and radius relationships
- Traditionally 43 triangles formed by intersections

## Torus Knot Parameters

`TorusKnot(p, q)` where p = windings around axis, q = windings through hole

Common sacred forms:
- (2, 3) - Trefoil knot
- (3, 2) - Figure-8 variant
- (5, 2) - Cinquefoil

## Interfaith Symbol Parameters

**Om (ॐ)**: SVG path or parametric curves for Devanagari rendering

**Star of David**: Two equilateral triangles, one rotated 180°
```
Triangle 1: angles 90°, 210°, 330° from center
Triangle 2: angles 270°, 30°, 150° from center
```

**Yin-Yang**: Two semicircles of diameter d, plus two small circles of diameter d/6

**Islamic 8-Point Star**: Octagon with vertices connected at 2-step intervals

**Christian Cross**: Golden ratio proportions - horizontal bar at φ position of vertical

**Buddhist Endless Knot**: Parametric interweaving loops, typically 3×3 grid base
