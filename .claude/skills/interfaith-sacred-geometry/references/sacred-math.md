# Sacred Mathematics Reference

## Fundamental Ratios

### Golden Ratio (φ)
```
φ = (1 + √5) / 2 ≈ 1.618033988749895

Properties:
- φ² = φ + 1
- 1/φ = φ - 1
- φⁿ = φⁿ⁻¹ + φⁿ⁻²
```

**Applications:**
- Spiral arm expansion
- Pentagon/pentagram construction
- Golden rectangle proportions
- Human body proportions (da Vinci)

### Silver Ratio (δ)
```
δ = 1 + √2 ≈ 2.414213562373095
```

**Applications:**
- Octagonal geometry
- Pell number sequences
- Islamic geometric patterns

### Sacred Numbers

| Number | Significance |
|--------|-------------|
| 1 | Unity, the One |
| 3 | Trinity, beginning-middle-end |
| 4 | Elements, directions, stability |
| 5 | Humanity (5 senses, 5 fingers) |
| 6 | Creation (6 days), harmony |
| 7 | Perfection, completion |
| 8 | Regeneration, infinity |
| 9 | Completion of cycle |
| 10 | Totality |
| 12 | Cosmic order (zodiac, apostles) |
| 40 | Testing, transformation |
| 108 | Sacred in Hinduism/Buddhism |

## Geometric Constructions

### Vesica Piscis
Two circles of radius r, centers distance r apart.

```
Intersection points: (0, ±√3·r/2)
Width of vesica: r
Height of vesica: √3·r ≈ 1.732·r
Ratio height/width: √3
```

The vesica generates:
- Equilateral triangle
- Fish (ichthys) shape
- Pointed oval (mandorla)

### Flower of Life
```python
def flower_of_life_centers(radius, rings=3):
    """Generate circle centers for Flower of Life."""
    centers = [(0, 0)]  # Central circle
    
    for ring in range(1, rings + 1):
        if ring == 1:
            # First ring: 6 circles at distance r
            for i in range(6):
                angle = i * π/3
                centers.append((radius * cos(angle), radius * sin(angle)))
        else:
            # Subsequent rings: more complex pattern
            # Each ring adds circles at intersections
            pass
    
    return centers
```

### Sri Yantra
9 interlocking triangles (4 upward, 5 downward) around central bindu.

**Construction method:**
1. Start with outer square (bhupura)
2. Draw 3 concentric circles
3. Position 9 triangles with vertices on specific radii
4. Central point (bindu) represents ultimate reality

Traditional proportions use complex calculations—see specialized texts.

### Metatron's Cube
13 circles: 1 center + 6 inner + 6 outer (offset 30°)

```python
def metatrons_cube(radius):
    circles = [(0, 0, radius * 0.3)]  # center
    
    # Inner ring
    for i in range(6):
        angle = i * π/3
        circles.append((radius * cos(angle), radius * sin(angle), radius * 0.3))
    
    # Outer ring (offset 30°)
    for i in range(6):
        angle = i * π/3 + π/6
        circles.append((2*radius * cos(angle), 2*radius * sin(angle), radius * 0.3))
    
    return circles
```

Connect all 13 centers with lines to reveal Platonic solids.

## Spiral Formulas

### Archimedean Spiral
```
r = a + bθ

Constant spacing between arms.
Used in: Labyrinths, Celtic patterns
```

### Logarithmic (Golden) Spiral
```
r = ae^(bθ)

For golden spiral: b = ln(φ) / (π/2) ≈ 0.3063

Self-similar at any scale.
Used in: Nautilus shells, galaxy arms, sacred growth patterns
```

### Fibonacci Spiral
```
Quarter circles with radii: 1, 1, 2, 3, 5, 8, 13, 21...
Each quarter arc connects to form continuous spiral.
Approximates golden spiral.
```

## Platonic Solids

| Solid | Faces | Vertices | Edges | Element |
|-------|-------|----------|-------|---------|
| Tetrahedron | 4 triangles | 4 | 6 | Fire |
| Cube | 6 squares | 8 | 12 | Earth |
| Octahedron | 8 triangles | 6 | 12 | Air |
| Dodecahedron | 12 pentagons | 20 | 30 | Ether/Spirit |
| Icosahedron | 20 triangles | 12 | 30 | Water |

**Euler's formula**: V - E + F = 2

**Duality pairs:**
- Tetrahedron ↔ Tetrahedron (self-dual)
- Cube ↔ Octahedron
- Dodecahedron ↔ Icosahedron

## Star Polygons

**{n/k} notation**: n points, connect every kth point

| Symbol | Notation | Construction |
|--------|----------|--------------|
| Pentagram | {5/2} | 5 points, skip 1 |
| Hexagram | {6/2} | Two overlapping triangles |
| Octagram | {8/3} | 8 points, skip 2 |

**Star of David (hexagram):**
```
Triangle 1 vertices: (0, r), (r·√3/2, -r/2), (-r·√3/2, -r/2)
Triangle 2 vertices: (0, -r), (r·√3/2, r/2), (-r·√3/2, r/2)
```

## Angular Relationships

**Division of circle:**
```
2 parts: 180° (duality)
3 parts: 120° (trinity)
4 parts: 90° (quadrants)
5 parts: 72° (pentagram)
6 parts: 60° (hexagram)
7 parts: 51.43° (septagram)
8 parts: 45° (octagram)
9 parts: 40° (enneagram)
10 parts: 36° (decagram)
12 parts: 30° (zodiac)
```
