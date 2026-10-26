# Font Pairing Guide

Principles and examples for combining typefaces effectively.

## Pairing Principles

### Contrast Creates Interest

Pair fonts that differ in:
- **Classification**: Serif + sans-serif
- **Weight**: Light heading + bold body (or vice versa)
- **Width**: Condensed + regular
- **Era**: Modern + traditional

### Harmony Maintains Unity

Paired fonts should share:
- **x-height**: Similar proportions
- **Mood**: Both formal, both casual, etc.
- **Quality**: Both professional-grade

### Hierarchy Guides Reading

- **Headings**: More personality, larger, bolder
- **Body**: More neutral, optimized for reading
- **Accents**: Distinct but not distracting

## Classification Pairings

### Serif + Sans-Serif (Classic)

```
Heading: Playfair Display (serif)
Body: Source Sans Pro (sans-serif)
Why: High contrast, editorial elegance
```

```
Heading: Lora (serif)
Body: Roboto (sans-serif)
Why: Warm readability meets modern clarity
```

### Sans-Serif + Sans-Serif (Modern)

```
Heading: Montserrat (geometric)
Body: Open Sans (humanist)
Why: Both modern, subtle contrast in structure
```

```
Heading: Poppins (geometric)
Body: Inter (neutral)
Why: Friendly heading with readable body
```

### Display + Text (Creative)

```
Heading: Abril Fatface (display serif)
Body: Lato (sans-serif)
Why: Statement heading with neutral body
```

```
Heading: Bebas Neue (display sans)
Body: Source Sans Pro (sans-serif)
Why: Bold headlines with clean body
```

## By Mood

### Professional/Corporate

| Heading | Body | Notes |
|---------|------|-------|
| Montserrat | Open Sans | Clean, trustworthy |
| Raleway | Lato | Refined, approachable |
| Source Sans Pro | Source Sans Pro | Consistent, neutral |

### Creative/Playful

| Heading | Body | Notes |
|---------|------|-------|
| Abril Fatface | Nunito | Statement + friendly |
| Lobster | Cabin | Script + readable |
| Fredoka One | Quicksand | Rounded + soft |

### Editorial/Elegant

| Heading | Body | Notes |
|---------|------|-------|
| Playfair Display | Source Sans Pro | Classic magazine |
| Cormorant Garamond | Proza Libre | Literary |
| Libre Baskerville | Karla | Traditional + modern |

### Technical/Developer

| Heading | Body | Mono |
|---------|------|------|
| IBM Plex Sans | IBM Plex Sans | IBM Plex Mono |
| JetBrains Mono | Inter | JetBrains Mono |
| Fira Sans | Fira Sans | Fira Code |

### Minimalist

| Heading | Body | Notes |
|---------|------|-------|
| Inter | Inter | Single font, weight variation |
| Helvetica Neue | Helvetica Neue | Classic Swiss |
| Work Sans | Work Sans | Geometric consistency |

## Weight & Size Guidelines

### Desktop

| Element | Size | Weight |
|---------|------|--------|
| H1 | 48-72px | Bold (700) |
| H2 | 36-48px | Semi-bold (600) |
| H3 | 24-36px | Medium (500) |
| Body | 16-18px | Regular (400) |
| Small | 14px | Regular (400) |
| Caption | 12px | Light (300) |

### Presentations

| Element | Size | Notes |
|---------|------|-------|
| Title | 60-80pt | One line max |
| Subtitle | 32-40pt | Below title |
| Section header | 40-48pt | Slide titles |
| Body | 24-32pt | Main content |
| Footnotes | 14-18pt | Citations, notes |

## Common Mistakes

### Avoid

- **Too similar**: Pairing fonts that look nearly identical
- **Too many**: Using more than 2-3 typefaces
- **Wrong weights**: Light headings with bold body
- **Competing styles**: Two decorative fonts together
- **Scale mismatch**: Fonts with very different x-heights

### Fix

- Create clear visual hierarchy
- Use one font family for simplicity
- Reserve decorative fonts for headings only
- Test at actual viewing sizes
- Compare side-by-side before committing

## Font Stack Recommendations

### Web-Safe Stacks

```css
/* Sans-serif */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
             "Helvetica Neue", Arial, sans-serif;

/* Serif */
font-family: Georgia, Cambria, "Times New Roman", Times, serif;

/* Mono */
font-family: "SF Mono", SFMono-Regular, Consolas,
             "Liberation Mono", Menlo, monospace;
```

### Google Fonts Priority

Load only weights you use:
```html
<!-- Optimal: 2-3 weights per font -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
```

## Quick Decision Tree

```
What's the primary mood?
├── Professional/Serious
│   └── Pair neutral sans-serifs OR serif heading + sans body
├── Creative/Expressive
│   └── Use display heading + clean body
├── Technical/Functional
│   └── Single sans-serif family, vary weights
└── Editorial/Literary
    └── Serif heading + humanist sans body
```
