# Theme Template

Standard structure for creating new themes.

## Theme File Format

```yaml
name: Theme Name
description: Brief description of the theme's mood and use case

colors:
  primary: "#HEXCODE"      # Main brand/accent color
  secondary: "#HEXCODE"    # Supporting accent
  background: "#HEXCODE"   # Page/slide background
  surface: "#HEXCODE"      # Card/container backgrounds
  text_primary: "#HEXCODE" # Main body text
  text_secondary: "#HEXCODE" # Muted/secondary text
  accent: "#HEXCODE"       # Highlights, links, CTAs

fonts:
  heading: "Font Name"     # Headers, titles
  body: "Font Name"        # Body text, paragraphs
  mono: "Font Name"        # Code, technical (optional)

characteristics:
  mood: "Keyword, Keyword" # 2-3 mood descriptors
  industry_fit: ["Industry1", "Industry2"]
  contrast_level: "high|medium|low"
  formality: "formal|semi-formal|casual"
```

## Color Selection Guidelines

### Contrast Requirements

| Combination | Minimum Ratio | WCAG Level |
|-------------|---------------|------------|
| Text on background | 4.5:1 | AA |
| Large text on background | 3:1 | AA |
| UI components | 3:1 | AA |

### Harmony Patterns

**Monochromatic**: Single hue, varied saturation/brightness
- Safe, cohesive, professional
- Risk: Can be monotonous

**Complementary**: Opposite hues
- High contrast, vibrant
- Risk: Can clash if saturations too high

**Analogous**: Adjacent hues
- Harmonious, natural
- Risk: May lack contrast

**Triadic**: Three evenly-spaced hues
- Balanced, colorful
- Risk: Can feel busy

### Role-Based Selection

1. **Background**: Usually lightest or darkest
2. **Surface**: Slight contrast from background
3. **Primary**: Brand identity, used sparingly
4. **Secondary**: Supports primary, less saturated
5. **Text**: High contrast with background
6. **Accent**: Small highlights, calls to action

## Font Pairing Guidelines

### Classic Combinations

| Heading | Body | Style |
|---------|------|-------|
| Serif | Sans-serif | Traditional, editorial |
| Sans-serif | Sans-serif | Modern, clean |
| Display | Sans-serif | Creative, bold |
| Slab serif | Sans-serif | Strong, contemporary |

### Font Characteristics

**Headings should be**:
- Distinctive, memorable
- Clear at large sizes
- Appropriate weight options

**Body should be**:
- Highly readable at small sizes
- Neutral (doesn't distract)
- Good x-height
- Multiple weights available

### Safe Font Combinations

| Heading | Body | Mood |
|---------|------|------|
| Playfair Display | Source Sans Pro | Elegant |
| Montserrat | Open Sans | Modern |
| Raleway | Lato | Clean |
| Merriweather | Roboto | Readable |
| Oswald | Noto Sans | Bold |
| Lora | Inter | Refined |

## Theme Checklist

Before finalizing a theme:

- [ ] Primary text readable on background (4.5:1+)
- [ ] Secondary text readable (3:1+ for decorative)
- [ ] Accent color visible against background
- [ ] Surface color distinguishable from background
- [ ] Colors harmonious when viewed together
- [ ] Fonts available (Google Fonts preferred)
- [ ] Heading font readable at H1-H6 sizes
- [ ] Body font readable at 14-18px
- [ ] Theme works in light conditions
- [ ] Theme works in dark conditions (if applicable)

## Example Theme

```yaml
name: Ocean Depths
description: Professional and calming maritime theme suitable for
             corporate presentations, environmental topics, or wellness brands

colors:
  primary: "#0077B6"       # Deep ocean blue
  secondary: "#00B4D8"     # Lighter teal
  background: "#FFFFFF"    # Clean white
  surface: "#CAF0F8"       # Pale sky blue
  text_primary: "#03045E"  # Dark navy
  text_secondary: "#0096C7" # Medium blue
  accent: "#48CAE4"        # Bright cyan

fonts:
  heading: "Poppins"
  body: "Open Sans"
  mono: "Fira Code"

characteristics:
  mood: "Calm, Professional, Trustworthy"
  industry_fit: ["Technology", "Healthcare", "Environmental"]
  contrast_level: "high"
  formality: "semi-formal"
```

## Quick Theme Generation Process

1. **Identify mood**: What feeling should this evoke?
2. **Choose base color**: What's the dominant hue?
3. **Build palette**: Add complementary/analogous colors
4. **Test contrast**: Verify accessibility
5. **Select heading font**: Match mood (serious/playful)
6. **Select body font**: Prioritize readability
7. **Test application**: Apply to sample content
8. **Refine**: Adjust based on actual use
