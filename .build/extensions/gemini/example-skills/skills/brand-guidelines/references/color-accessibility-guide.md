# Color Accessibility Guide

Ensuring brand colors meet accessibility standards.

## WCAG Contrast Requirements

### Minimum Ratios

| Level | Normal Text | Large Text | UI Components |
|-------|-------------|------------|---------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | 4.5:1 |

**Large text**: 18pt regular or 14pt bold

---

## Anthropic Brand Color Contrast

### Dark on Light Backgrounds

| Foreground | Background | Ratio | AA | AAA |
|------------|------------|-------|----|----|
| Dark #141413 | Light #faf9f5 | 17.8:1 | Pass | Pass |
| Dark #141413 | Light Gray #e8e6dc | 13.2:1 | Pass | Pass |
| Dark #141413 | Mid Gray #b0aea5 | 6.1:1 | Pass | Fail |

### Light on Dark Backgrounds

| Foreground | Background | Ratio | AA | AAA |
|------------|------------|-------|----|----|
| Light #faf9f5 | Dark #141413 | 17.8:1 | Pass | Pass |
| Light Gray #e8e6dc | Dark #141413 | 13.2:1 | Pass | Pass |
| Mid Gray #b0aea5 | Dark #141413 | 6.1:1 | Pass | Fail |

### Accent Colors

| Foreground | Background | Ratio | AA Text | Large Text |
|------------|------------|-------|---------|------------|
| Orange #d97757 | Dark #141413 | 4.9:1 | Pass | Pass |
| Orange #d97757 | Light #faf9f5 | 3.6:1 | Fail | Pass |
| Blue #6a9bcc | Dark #141413 | 6.2:1 | Pass | Pass |
| Blue #6a9bcc | Light #faf9f5 | 2.9:1 | Fail | Fail |
| Green #788c5d | Dark #141413 | 4.7:1 | Pass | Pass |
| Green #788c5d | Light #faf9f5 | 3.8:1 | Fail | Pass |

---

## Safe Color Combinations

### For Body Text (Small)

| Combination | Use |
|-------------|-----|
| Dark on Light | Primary body text |
| Light on Dark | Inverted sections |
| Dark on Light Gray | Secondary content |

### For Headings (Large Text)

| Combination | Use |
|-------------|-----|
| All above, plus: | |
| Orange on Dark | Accent headings |
| Green on Dark | Category labels |
| Blue on Dark | Links, highlights |

### For UI Elements

| Combination | Use |
|-------------|-----|
| Orange on Dark | Buttons, CTAs |
| Dark on Orange | Alternative buttons |
| Accents on Dark | Icons, badges |

---

## Accent Color Usage Guidelines

### Orange #d97757

```
DO: Use on dark backgrounds for CTAs
DO: Use for emphasis, highlights
DO: Use as button background with light text
DON'T: Use for body text on light backgrounds
DON'T: Use for small text anywhere
```

### Blue #6a9bcc

```
DO: Use on dark backgrounds
DO: Use for links on dark backgrounds
DO: Use for decorative elements
DON'T: Use for text on light backgrounds
DON'T: Rely on color alone for meaning
```

### Green #788c5d

```
DO: Use on dark backgrounds
DO: Use for success states (with icon)
DO: Use as accent in charts
DON'T: Use for critical text on light
DON'T: Use as only indicator of success
```

---

## Accessible Design Patterns

### Links

```css
/* Accessible link styling */
.link {
  color: #141413;  /* Dark on light */
  text-decoration: underline;  /* Not just color */
}

.link-on-dark {
  color: #6a9bcc;  /* Blue on dark */
  text-decoration: underline;
}
```

### Buttons

```css
/* Primary button */
.btn-primary {
  background: #d97757;  /* Orange */
  color: #faf9f5;  /* Light */
  /* 4.9:1 ratio - passes AA */
}

/* Secondary button */
.btn-secondary {
  background: #141413;  /* Dark */
  color: #faf9f5;  /* Light */
  /* 17.8:1 ratio - passes AAA */
}
```

### Error States

```css
/* Don't rely on color alone */
.error {
  color: #d97757;
  border-left: 4px solid #d97757;
  /* Also use icon and clear text */
}
```

---

## Testing Tools

### Online Checkers

| Tool | URL | Use |
|------|-----|-----|
| WebAIM Contrast Checker | webaim.org/resources/contrastchecker | Quick checks |
| Coolors Contrast Checker | coolors.co/contrast-checker | Visual preview |
| Adobe Color | color.adobe.com/create/color-accessibility | Full palette |

### Browser Extensions

- axe DevTools
- WAVE Evaluation Tool
- Color Contrast Analyzer

### Simulation Tools

Check for color blindness visibility:
- Deuteranopia (red-green)
- Protanopia (red-green)
- Tritanopia (blue-yellow)

---

## Fallback Strategies

### When Contrast Fails

1. **Add visual cues**: Icons, patterns, borders
2. **Adjust background**: Use darker/lighter variant
3. **Increase text size**: Large text has lower requirements
4. **Add text shadow**: Subtle shadow improves readability
5. **Use solid background**: Behind text on images

### Example Fixes

```
BEFORE: Blue text on light gray (2.9:1 - fails)
AFTER: Blue text on dark background (6.2:1 - passes)

BEFORE: Orange for error text only
AFTER: Orange + warning icon + border
```

---

## Quick Reference Card

### Always Safe

| Purpose | Combination |
|---------|-------------|
| Body text | Dark (#141413) on Light (#faf9f5) |
| Inverted text | Light (#faf9f5) on Dark (#141413) |
| Primary buttons | Light text on Orange or Dark |
| Secondary buttons | Dark text on Light Gray |

### Use With Caution

| Purpose | Combination | Note |
|---------|-------------|------|
| Accent headings | Orange on Light | Large text only |
| Links on dark | Blue on Dark | Underline required |
| Success states | Green on Dark | Add icon |

### Avoid

| Combination | Issue |
|-------------|-------|
| Blue text on light | 2.9:1 fails |
| Accent colors for small text on light | Insufficient contrast |
| Color-only differentiation | Fails accessibility |
