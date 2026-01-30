#!/usr/bin/env python3
"""
Sacred Geometry Vertex Generator
Outputs JSON arrays of vertices for Three.js BufferGeometry
"""

import json
import math
from typing import List, Tuple

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio


def flower_of_life(radius: float = 1.0, rings: int = 2) -> dict:
    """Generate Flower of Life circle centers and radii."""
    circles = [{"x": 0, "y": 0, "r": radius}]
    
    for ring in range(1, rings + 1):
        count = 6 * ring
        ring_radius = radius * ring
        for i in range(count):
            angle = (2 * math.pi * i) / count
            circles.append({
                "x": ring_radius * math.cos(angle),
                "y": ring_radius * math.sin(angle),
                "r": radius
            })
    
    return {"type": "flower_of_life", "circles": circles}


def metatrons_cube(radius: float = 1.0) -> dict:
    """Generate Metatron's Cube with 13 circles and connecting lines."""
    circles = [{"x": 0, "y": 0, "r": radius * 0.3}]
    
    # Inner ring (6 circles)
    for i in range(6):
        angle = (2 * math.pi * i) / 6
        circles.append({
            "x": radius * math.cos(angle),
            "y": radius * math.sin(angle),
            "r": radius * 0.3
        })
    
    # Outer ring (6 circles, offset by 30°)
    for i in range(6):
        angle = (2 * math.pi * i) / 6 + math.pi / 6
        circles.append({
            "x": 2 * radius * math.cos(angle),
            "y": 2 * radius * math.sin(angle),
            "r": radius * 0.3
        })
    
    # Generate all connecting lines between circle centers
    lines = []
    centers = [(c["x"], c["y"]) for c in circles]
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            lines.append({
                "start": {"x": centers[i][0], "y": centers[i][1]},
                "end": {"x": centers[j][0], "y": centers[j][1]}
            })
    
    return {"type": "metatrons_cube", "circles": circles, "lines": lines}


def golden_spiral(loops: int = 3, points_per_loop: int = 100, scale: float = 1.0) -> dict:
    """Generate golden spiral vertices."""
    points = []
    total_points = loops * points_per_loop
    
    for i in range(total_points):
        theta = (i / points_per_loop) * 2 * math.pi
        r = scale * (PHI ** (theta / (2 * math.pi)))
        points.append({
            "x": r * math.cos(theta),
            "y": r * math.sin(theta),
            "z": 0
        })
    
    return {"type": "golden_spiral", "points": points}


def platonic_solid(solid_type: str) -> dict:
    """Generate vertices and faces for Platonic solids."""
    solids = {
        "tetrahedron": {
            "vertices": [
                (1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)
            ],
            "faces": [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)]
        },
        "cube": {
            "vertices": [
                (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
            ],
            "faces": [
                (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
                (2, 6, 7, 3), (0, 3, 7, 4), (1, 5, 6, 2)
            ]
        },
        "octahedron": {
            "vertices": [
                (1, 0, 0), (-1, 0, 0), (0, 1, 0),
                (0, -1, 0), (0, 0, 1), (0, 0, -1)
            ],
            "faces": [
                (0, 2, 4), (0, 4, 3), (0, 3, 5), (0, 5, 2),
                (1, 4, 2), (1, 3, 4), (1, 5, 3), (1, 2, 5)
            ]
        },
        "icosahedron": {
            "vertices": [
                (0, 1, PHI), (0, -1, PHI), (0, 1, -PHI), (0, -1, -PHI),
                (1, PHI, 0), (-1, PHI, 0), (1, -PHI, 0), (-1, -PHI, 0),
                (PHI, 0, 1), (-PHI, 0, 1), (PHI, 0, -1), (-PHI, 0, -1)
            ],
            "faces": [
                (0, 1, 8), (0, 8, 4), (0, 4, 5), (0, 5, 9), (0, 9, 1),
                (1, 6, 8), (8, 6, 10), (8, 10, 4), (4, 10, 2), (4, 2, 5),
                (5, 2, 11), (5, 11, 9), (9, 11, 7), (9, 7, 1), (1, 7, 6),
                (3, 6, 7), (3, 7, 11), (3, 11, 2), (3, 2, 10), (3, 10, 6)
            ]
        },
        "dodecahedron": {
            "vertices": [
                (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
                (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
                (0, 1/PHI, PHI), (0, 1/PHI, -PHI), (0, -1/PHI, PHI), (0, -1/PHI, -PHI),
                (1/PHI, PHI, 0), (-1/PHI, PHI, 0), (1/PHI, -PHI, 0), (-1/PHI, -PHI, 0),
                (PHI, 0, 1/PHI), (PHI, 0, -1/PHI), (-PHI, 0, 1/PHI), (-PHI, 0, -1/PHI)
            ],
            "faces": [
                (0, 8, 10, 2, 16), (0, 16, 17, 1, 12), (0, 12, 13, 4, 8),
                (1, 17, 3, 11, 9), (1, 9, 5, 13, 12), (2, 10, 6, 15, 14),
                (2, 14, 3, 17, 16), (3, 14, 15, 7, 11), (4, 13, 5, 19, 18),
                (4, 18, 6, 10, 8), (5, 9, 11, 7, 19), (6, 18, 19, 7, 15)
            ]
        }
    }
    
    if solid_type not in solids:
        raise ValueError(f"Unknown solid: {solid_type}. Options: {list(solids.keys())}")
    
    data = solids[solid_type]
    return {
        "type": solid_type,
        "vertices": [{"x": v[0], "y": v[1], "z": v[2]} for v in data["vertices"]],
        "faces": data["faces"]
    }


def star_polygon(points: int = 6, outer_radius: float = 1.0, inner_radius: float = 0.5) -> dict:
    """Generate star polygon vertices (like Star of David with points=6)."""
    vertices = []
    
    for i in range(points * 2):
        angle = (math.pi * i) / points - math.pi / 2
        radius = outer_radius if i % 2 == 0 else inner_radius
        vertices.append({
            "x": radius * math.cos(angle),
            "y": radius * math.sin(angle),
            "z": 0
        })
    
    return {"type": f"star_{points}", "vertices": vertices}


def torus_knot_points(p: int = 2, q: int = 3, radius: float = 1.0, 
                       tube_radius: float = 0.3, segments: int = 200) -> dict:
    """Generate torus knot centerline points."""
    points = []
    
    for i in range(segments):
        t = (i / segments) * 2 * math.pi * p
        
        r = radius + tube_radius * math.cos(q * t / p)
        x = r * math.cos(t)
        y = r * math.sin(t)
        z = tube_radius * math.sin(q * t / p)
        
        points.append({"x": x, "y": y, "z": z})
    
    return {"type": f"torus_knot_{p}_{q}", "points": points}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: sacred_geometry.py <type> [params...]")
        print("Types: flower, metatron, spiral, platonic, star, torus")
        sys.exit(1)
    
    geom_type = sys.argv[1]
    
    if geom_type == "flower":
        rings = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        result = flower_of_life(rings=rings)
    elif geom_type == "metatron":
        result = metatrons_cube()
    elif geom_type == "spiral":
        loops = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        result = golden_spiral(loops=loops)
    elif geom_type == "platonic":
        solid = sys.argv[2] if len(sys.argv) > 2 else "icosahedron"
        result = platonic_solid(solid)
    elif geom_type == "star":
        points = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        result = star_polygon(points=points)
    elif geom_type == "torus":
        p = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        q = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        result = torus_knot_points(p=p, q=q)
    else:
        print(f"Unknown type: {geom_type}")
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
