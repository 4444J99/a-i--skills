# Curated Color Palettes

Ready-to-use palettes for generative art.

## Classic Generative Art Palettes

### Deep Ocean

```javascript
const deepOcean = ['#05445E', '#189AB4', '#75E6DA', '#D4F1F9'];
// Dark navy → teal → aqua → pale blue
```

### Sunset Gradient

```javascript
const sunset = ['#FF6B6B', '#FEC89A', '#FFD93D', '#6BCB77'];
// Coral → peach → golden → soft green
```

### Monochrome Ink

```javascript
const ink = ['#1A1A2E', '#16213E', '#0F3460', '#E94560'];
// Deep blacks with single accent
```

### Forest Depths

```javascript
const forest = ['#1B4332', '#2D6A4F', '#40916C', '#95D5B2'];
// Dark forest → moss → sage → mint
```

### Cosmic Purple

```javascript
const cosmic = ['#10002B', '#240046', '#5A189A', '#9D4EDD'];
// Near black → deep purple → violet → lavender
```

## Earthy & Natural

### Desert Sand

```javascript
const desert = ['#E9D8A6', '#EE9B00', '#CA6702', '#9B2226'];
// Sand → amber → burnt orange → rust
```

### Stone

```javascript
const stone = ['#D4CFC9', '#9C9990', '#6D6A66', '#3C3A36'];
// Warm grays from light to dark
```

### Autumn

```javascript
const autumn = ['#582F0E', '#7F4F24', '#B08968', '#DDB892'];
// Rich browns → tans
```

### Moss & Lichen

```javascript
const moss = ['#606C38', '#283618', '#FEFAE0', '#DDA15E'];
// Olive → dark green → cream → ochre
```

## Vibrant & Pop

### Neon Night

```javascript
const neon = ['#F72585', '#7209B7', '#3A0CA3', '#4CC9F0'];
// Hot pink → purple → indigo → cyan
```

### Rainbow Spectrum

```javascript
const rainbow = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#8B00FF'];
// Classic ROYGBV
```

### Candy

```javascript
const candy = ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#BDB2FF'];
// Soft pastels, high saturation
```

### Electric

```javascript
const electric = ['#00F5D4', '#00BBF9', '#9B5DE5', '#F15BB5'];
// Cyan → blue → purple → pink
```

## Minimal & Sophisticated

### Swiss

```javascript
const swiss = ['#FFFFFF', '#FF0000', '#000000'];
// White, red, black—maximum contrast
```

### Bauhaus

```javascript
const bauhaus = ['#1B1B1E', '#D64045', '#EAC435', '#5386E4'];
// Black + primary colors
```

### Paper

```javascript
const paper = ['#F7F3E9', '#E8E4DA', '#C4C1B7', '#3D3D3D'];
// Off-whites → warm gray → charcoal
```

### Noir

```javascript
const noir = ['#0D0D0D', '#1A1A1A', '#333333', '#F5F5F5'];
// Deep blacks with stark white accent
```

## Pastel Collections

### Soft Dawn

```javascript
const softDawn = ['#FEC5BB', '#FCD5CE', '#FAE1DD', '#F8EDEB'];
// Graduated soft pinks
```

### Ice Cream

```javascript
const iceCream = ['#B8F3FF', '#FFE4E1', '#FFFDD7', '#E1FFE8'];
// Mint → pink → cream → pistachio
```

### Muted Rainbow

```javascript
const muted = ['#F28482', '#F5CAC3', '#84A59D', '#F7EDE2'];
// Desaturated coral, sage, cream
```

## Using Palettes in Code

### Random from Palette

```javascript
function randomColor(palette) {
  return palette[floor(random(palette.length))];
}
```

### Noise-Based Selection

```javascript
function noiseColor(x, y, palette, scale) {
  let n = noise(x * scale, y * scale);
  let index = floor(n * palette.length);
  return palette[constrain(index, 0, palette.length - 1)];
}
```

### Gradient Along Palette

```javascript
function gradientColor(t, palette) {
  // t: 0-1
  let scaled = t * (palette.length - 1);
  let index = floor(scaled);
  let blend = scaled - index;

  if (index >= palette.length - 1) return color(palette[palette.length - 1]);

  return lerpColor(
    color(palette[index]),
    color(palette[index + 1]),
    blend
  );
}
```

### Adding Transparency

```javascript
function withAlpha(hexColor, alpha) {
  let c = color(hexColor);
  c.setAlpha(alpha);
  return c;
}

// Usage
stroke(withAlpha(palette[0], 50));
```

## Palette Generation Techniques

### From Base Color

```javascript
function monochromaticPalette(baseHue, count) {
  colorMode(HSB);
  let palette = [];
  for (let i = 0; i < count; i++) {
    let saturation = map(i, 0, count - 1, 20, 80);
    let brightness = map(i, 0, count - 1, 90, 30);
    palette.push(color(baseHue, saturation, brightness));
  }
  return palette;
}
```

### Complementary Pair + Neutrals

```javascript
function complementaryPalette(hue) {
  colorMode(HSB);
  return [
    color(hue, 70, 85),
    color((hue + 180) % 360, 70, 85),
    color(hue, 10, 95),  // Near white
    color(hue, 5, 15)    // Near black
  ];
}
```

## Quick Reference Table

| Mood | Recommended Palettes |
|------|---------------------|
| Calm, meditative | deepOcean, moss, paper |
| Energetic, bold | neon, electric, candy |
| Natural, organic | forest, desert, autumn |
| Sophisticated | swiss, bauhaus, noir |
| Dreamy, soft | softDawn, iceCream, muted |
| Dark, moody | cosmic, ink, noir |
