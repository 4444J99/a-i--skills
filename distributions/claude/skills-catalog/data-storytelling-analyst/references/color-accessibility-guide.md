# Color Accessibility Guide

Ensure your data visualizations are readable by everyone.

## Color Blindness Basics

### Types and Prevalence

| Type | Affects | Prevalence |
|------|---------|------------|
| Deuteranopia | Green perception | 6% of males |
| Protanopia | Red perception | 2% of males |
| Tritanopia | Blue perception | <1% |
| Achromatopsia | All color | Very rare |

**Key stat**: ~8% of men and ~0.5% of women have some color vision deficiency.

## Safe Color Palettes

### Sequential (Ordered Data)

**Viridis** (default recommendation):
```
#440154 → #414487 → #2A788E → #22A884 → #7AD151 → #FDE725
```
- Perceptually uniform
- Works in grayscale
- Colorblind-safe

**Blues**:
```
#F7FBFF → #DEEBF7 → #C6DBEF → #9ECAE1 → #6BAED6 → #2171B5
```

**Greens**:
```
#F7FCF5 → #C7E9C0 → #74C476 → #31A354 → #006D2C
```

### Diverging (Centered Data)

**Blue-Red (Colorblind safe)**:
```
#2166AC → #67A9CF → #F7F7F7 → #EF8A62 → #B2182B
```

**Purple-Green**:
```
#762A83 → #C2A5CF → #F7F7F7 → #A6DBA0 → #1B7837
```

### Categorical (Distinct Groups)

**ColorBrewer Set2** (max 8 categories):
```
#66C2A5  #FC8D62  #8DA0CB  #E78AC3  #A6D854  #FFD92F  #E5C494  #B3B3B3
```

**Tableau 10** (colorblind-friendly):
```
#4E79A7  #F28E2B  #E15759  #76B7B2  #59A14F  #EDC948  #B07AA1  #FF9DA7
```

**IBM Carbon** (accessible):
```
#6929C4  #1192E8  #005D5D  #9F1853  #FA4D56  #570408  #198038  #002D9C
```

## Avoid These Combinations

### High Risk Pairs

| Combination | Problem | Alternative |
|-------------|---------|-------------|
| Red + Green | Most common CVD | Blue + Orange |
| Green + Brown | Difficult to distinguish | Blue + Yellow |
| Blue + Purple | Similar hue | Blue + Orange |
| Light green + Yellow | Low contrast | Dark green + Yellow |

### Better Alternatives

Instead of red/green:
- Blue/orange
- Blue/yellow
- Purple/yellow
- Dark blue/light orange

## Beyond Color

### Use Redundant Encoding

Don't rely on color alone:

```
Color + Shape:    ● ■ ▲ ◆
Color + Pattern:  solid, dashed, dotted
Color + Label:    Direct annotation
Color + Position: Group related items
```

### Texture and Pattern (Accessibility)

For filled areas:
- Solid
- Diagonal lines
- Dots
- Crosshatch
- Horizontal lines

For lines:
- Solid
- Dashed
- Dotted
- Dash-dot

## Contrast Requirements

### Text on Backgrounds

| Ratio | Use |
|-------|-----|
| 7:1 | Body text (WCAG AAA) |
| 4.5:1 | Large text minimum (WCAG AA) |
| 3:1 | Non-text elements |

### Chart Elements

| Element | Minimum Contrast |
|---------|------------------|
| Data vs background | 3:1 |
| Adjacent data colors | 3:1 |
| Labels vs background | 4.5:1 |
| Gridlines vs background | 1.5:1 (intentionally subtle) |

## Testing Your Visualization

### Tools

1. **Color Oracle** (Desktop): Simulates color blindness
2. **Viz Palette** (Web): Test palette accessibility
3. **Coblis** (Web): Color blindness simulator
4. **Chrome DevTools**: Emulate vision deficiencies

### Quick Tests

1. **Grayscale test**: Print/view in grayscale. Still readable?
2. **Squint test**: Blur your eyes. Can you still see patterns?
3. **5-second test**: Can someone get the main point quickly?

## Implementation Tips

### Python (Matplotlib/Seaborn)

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Use colorblind-friendly palette
sns.set_palette("colorblind")

# Or Viridis for sequential
plt.imshow(data, cmap='viridis')

# Accessible categorical
colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']
```

### R (ggplot2)

```r
library(ggplot2)
library(viridis)

# Viridis scale
scale_fill_viridis_d()
scale_color_viridis_c()

# ColorBrewer
scale_fill_brewer(palette = "Set2")
```

## Checklist

Before publishing:

- [ ] Tested with colorblind simulator
- [ ] Tested in grayscale
- [ ] Uses redundant encoding (not color alone)
- [ ] Contrast ratios meet minimums
- [ ] Legend or direct labels present
- [ ] Works in both light and dark contexts
