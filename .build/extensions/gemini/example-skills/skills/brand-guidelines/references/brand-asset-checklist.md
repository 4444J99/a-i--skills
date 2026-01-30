# Brand Asset Checklist

A comprehensive checklist for ensuring brand consistency across deliverables.

## Pre-Design Verification

### Color System

| Check | Item | Notes |
|-------|------|-------|
| [ ] | Primary colors defined | Dark #141413, Light #faf9f5 |
| [ ] | Accent colors confirmed | Orange #d97757, Blue #6a9bcc, Green #788c5d |
| [ ] | Color contrast verified | WCAG AA minimum for text |
| [ ] | Gradient usage defined | If gradients allowed, which combinations |

### Typography

| Check | Item | Notes |
|-------|------|-------|
| [ ] | Heading font confirmed | Poppins (Arial fallback) |
| [ ] | Body font confirmed | Lora (Georgia fallback) |
| [ ] | Fonts installed/accessible | Check rendering environment |
| [ ] | Size scale defined | Heading: 24pt+, Body: varies |
| [ ] | Line height specified | Typically 1.4-1.6 for body |

---

## Document Types

### Presentations

| Element | Requirement | Verified |
|---------|-------------|----------|
| Title slide | Company logo, dark background | [ ] |
| Section headers | Poppins, 28-36pt | [ ] |
| Body text | Lora, 18-24pt | [ ] |
| Accent elements | Use brand accent colors | [ ] |
| Footer | Consistent placement | [ ] |

### Web Content

| Element | Requirement | Verified |
|---------|-------------|----------|
| Headers (H1-H3) | Poppins font family | [ ] |
| Body paragraphs | Lora font family | [ ] |
| Links | Brand accent color | [ ] |
| Buttons | Brand colors with contrast | [ ] |
| Icons | Consistent style | [ ] |

### Print Materials

| Element | Requirement | Verified |
|---------|-------------|----------|
| Color mode | CMYK for print | [ ] |
| Resolution | 300 DPI minimum | [ ] |
| Bleed | 0.125" standard | [ ] |
| Safe zone | 0.25" from edges | [ ] |
| Font embedding | All fonts embedded | [ ] |

---

## Logo Usage

### Clear Space

```
Minimum clear space = height of logo "A"

    ┌─────────────────────┐
    │                     │
    │    ┌─────────┐      │
    │    │  LOGO   │      │
    │    └─────────┘      │
    │                     │
    └─────────────────────┘
```

### Logo Don'ts

| Issue | Description |
|-------|-------------|
| Stretching | Never distort proportions |
| Wrong colors | Use only approved color versions |
| Low resolution | Minimum 150 DPI for print |
| Busy backgrounds | Ensure sufficient contrast |
| Modifications | No shadows, outlines, or effects |

---

## Color Application

### Background + Text Combinations

| Background | Text Color | Use Case |
|------------|------------|----------|
| Dark (#141413) | Light (#faf9f5) | Hero sections, headers |
| Light (#faf9f5) | Dark (#141413) | Body content |
| Light Gray (#e8e6dc) | Dark (#141413) | Subtle sections |
| Accent Orange (#d97757) | Light (#faf9f5) | CTAs, buttons |

### Accent Usage

```
Primary content: Dark/Light only
Emphasis: Orange accent (sparingly)
Secondary elements: Blue or Green
Charts/Graphs: Cycle through accents
```

---

## File Naming Convention

### Standard Format

```
[project]_[asset-type]_[variant]_[date].[ext]

Examples:
- anthropic_presentation_final_20240115.pptx
- anthropic_logo_dark_2024.svg
- anthropic_banner_web_1200x628.png
```

### Version Control

| Suffix | Meaning |
|--------|---------|
| `_draft` | Work in progress |
| `_review` | Pending approval |
| `_final` | Approved version |
| `_v2`, `_v3` | Revision number |

---

## Export Checklist

### Digital Assets

| Format | Use Case | Settings |
|--------|----------|----------|
| PNG | Web, transparent backgrounds | sRGB, 72 DPI |
| JPG | Photos, social media | sRGB, 72 DPI, quality 80%+ |
| SVG | Logos, icons | Optimized, outlined text |
| PDF | Documents, shareable | Embed fonts, compress images |

### Print Assets

| Format | Use Case | Settings |
|--------|----------|----------|
| PDF | Print-ready | CMYK, 300 DPI, bleeds |
| TIFF | High-quality images | CMYK, 300 DPI |
| EPS | Vector artwork | Outlined fonts |

---

## Quality Assurance

### Final Review

| Check | Description |
|-------|-------------|
| [ ] | All colors match brand palette |
| [ ] | Fonts render correctly |
| [ ] | Logo usage follows guidelines |
| [ ] | Spelling and grammar checked |
| [ ] | Links functional (if digital) |
| [ ] | File size optimized |
| [ ] | Named correctly |
| [ ] | Proper format for destination |

### Accessibility

| Check | Description |
|-------|-------------|
| [ ] | Color contrast meets WCAG AA |
| [ ] | Text is readable at intended size |
| [ ] | Alt text for images (if applicable) |
| [ ] | Logical reading order |
