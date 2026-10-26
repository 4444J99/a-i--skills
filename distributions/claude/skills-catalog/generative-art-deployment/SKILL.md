---
name: generative-art-deployment
description: Deploy generative art projects for exhibition, web galleries, and print production. Covers rendering pipelines, resolution management, gallery hosting, and archival strategies for algorithmic artworks. Triggers on generative art deployment, art exhibition setup, or digital art publishing requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - generative-art
  - deployment
  - gallery
  - exhibition
  - archival
governance_phases: [build, prove]
organ_affinity: [organ-ii]
triggers: [user-asks-about-art-deployment, context:generative-art-exhibition, context:art-gallery, context:art-publishing]
complements: [generative-art-algorithms, three-js-interactive-builder, algorithmic-art, deployment-cicd]
---

# Generative Art Deployment

Move generative artworks from development to exhibition, print, and archive.

## Deployment Targets

| Target | Format | Resolution | Considerations |
|--------|--------|-----------|----------------|
| **Web gallery** | HTML/JS, WebGL | Screen (72-96 DPI) | Performance, loading time |
| **Physical print** | PNG/TIFF | 300 DPI minimum | Color profiles, bleed |
| **LED installation** | Video/WebGL | Panel-specific | Brightness, refresh rate |
| **NFT/on-chain** | PNG/SVG/HTML | Variable | File size, determinism |
| **Social media** | PNG/MP4 | Platform-specific | Compression, aspect ratio |
| **Archive** | Source + renders | Maximum | Reproducibility |

## Web Gallery Deployment

### Static Gallery Structure

```
gallery/
├── index.html          # Gallery grid/navigation
├── works/
│   ├── piece-001/
│   │   ├── index.html  # Full-screen viewer
│   │   ├── sketch.js   # Live generative code
│   │   ├── thumbnail.png
│   │   └── metadata.json
│   └── piece-002/
│       └── ...
├── assets/
│   ├── style.css
│   └── gallery.js
└── catalog.json        # Machine-readable catalog
```

### Work Metadata

```json
{
  "title": "Recursive Bloom #47",
  "artist": "Artist Name",
  "date": "2026-03-20",
  "medium": "Generative, p5.js",
  "dimensions": "3840 × 2160",
  "seed": 1742518400,
  "parameters": {
    "complexity": 0.7,
    "palette": "autumn",
    "iterations": 5000
  },
  "description": "An exploration of recursive growth patterns...",
  "series": "Recursive Bloom",
  "edition": "1/1",
  "tags": ["recursion", "organic", "growth"]
}
```

### Performance Optimization

```javascript
// Render once, display static
function setup() {
  const canvas = createCanvas(3840, 2160);
  noLoop(); // Don't animate
}

function draw() {
  randomSeed(SEED);
  // ... generate artwork
  saveCanvas('output', 'png');
}

// For interactive pieces: use requestAnimationFrame
// with quality degradation on low-end devices
function draw() {
  if (frameRate() < 30) {
    reduceComplexity();
  }
}
```

## Print Production

### Resolution Pipeline

```python
def render_for_print(sketch_path: str, width_inches: float, height_inches: float, dpi: int = 300):
    pixel_width = int(width_inches * dpi)
    pixel_height = int(height_inches * dpi)

    # Add bleed (0.125 inches on each side)
    bleed = int(0.125 * dpi)
    total_width = pixel_width + 2 * bleed
    total_height = pixel_height + 2 * bleed

    return {
        "canvas_width": total_width,
        "canvas_height": total_height,
        "safe_area": {
            "x": bleed, "y": bleed,
            "width": pixel_width, "height": pixel_height,
        },
        "dpi": dpi,
        "format": "TIFF",  # Lossless for print
        "color_profile": "sRGB",  # Or Adobe RGB for wide gamut
    }
```

### Color Management

```python
from PIL import Image, ImageCms

def convert_for_print(input_path: str, output_path: str):
    img = Image.open(input_path)
    srgb_profile = ImageCms.createProfile("sRGB")
    # For fine art printing, embed the ICC profile
    img.save(output_path, "TIFF", dpi=(300, 300), icc_profile=ImageCms.ImageCmsProfile(srgb_profile).tobytes())
```

### Print Sizes

| Size | Inches | Pixels (300 DPI) |
|------|--------|-------------------|
| A4 | 8.3 × 11.7 | 2490 × 3510 |
| A3 | 11.7 × 16.5 | 3510 × 4950 |
| A2 | 16.5 × 23.4 | 4950 × 7020 |
| 24×36 poster | 24 × 36 | 7200 × 10800 |

## Rendering Pipeline

### Batch Rendering

```python
import subprocess
from pathlib import Path

def batch_render(sketch: str, seeds: list[int], output_dir: str, width: int, height: int):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for seed in seeds:
        output = f"{output_dir}/render_{seed:08d}.png"
        subprocess.run([
            "node", sketch,
            "--seed", str(seed),
            "--width", str(width),
            "--height", str(height),
            "--output", output,
        ], check=True)

# Render a series
batch_render("sketch.js", seeds=range(1, 101), output_dir="renders/series-01", width=3840, height=2160)
```

### Deterministic Rendering

```javascript
// Ensure reproducibility: same seed = same output
function setup() {
  const seed = parseInt(getURLParam('seed') || '42');
  randomSeed(seed);
  noiseSeed(seed);
  // Record seed in metadata
  document.title = `Piece #${seed}`;
}
```

## Exhibition Patterns

### Installation Checklist

- [ ] Hardware specs confirmed (GPU, resolution, orientation)
- [ ] Autostart on boot configured
- [ ] Crash recovery (watchdog/supervisor process)
- [ ] No UI chrome (cursor hidden, fullscreen)
- [ ] Network not required (all assets local)
- [ ] Power failure recovery tested

### Kiosk Mode Setup

```bash
# Linux kiosk mode
#!/usr/bin/env bash
xset -dpms          # Disable power management
xset s off           # Disable screen saver
unclutter -idle 0.5 & # Hide cursor

chromium-browser \
  --kiosk \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --noerrdialogs \
  file:///home/gallery/piece/index.html
```

## Archival Strategy

### Archive Package

```
archive/
├── README.md           # How to run this piece
├── source/             # Original source code
│   ├── sketch.js
│   └── package.json
├── renders/            # High-res rendered outputs
│   ├── render_001.tiff
│   └── render_001.png
├── metadata.json       # Full metadata including parameters
├── dependencies/       # Vendored dependencies
│   └── p5.min.js
└── documentation/
    ├── process.md      # Artist statement, process notes
    └── screenshots/    # Exhibition documentation
```

### Reproducibility Contract

```json
{
  "runtime": "node 20.x + p5.js 1.9.x",
  "seed": 42,
  "canvas": "3840x2160",
  "parameters": {},
  "checksum": "sha256:abc123...",
  "rendered": "2026-03-20T10:00:00Z"
}
```

## Anti-Patterns

- **No seed recorded** — Every generative piece must have a reproducible seed
- **Web-only renders** — Always produce high-res static renders for print/archive
- **Missing metadata** — Parameters, dimensions, and creation date are essential
- **No offline fallback** — Exhibition pieces must work without network
- **Lossy-only archives** — Keep lossless TIFF/PNG alongside compressed versions
- **Undocumented dependencies** — Vendor or lockfile all runtime dependencies
