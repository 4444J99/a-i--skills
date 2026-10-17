# Slide Design Patterns

Templates and principles for effective presentation slides.

## Core Design Principles

### The Assertion-Evidence Model

Replace traditional title-and-bullets slides with:

```
┌──────────────────────────────────────┐
│ Full-sentence assertion as headline  │
│                                      │
│         Visual evidence              │
│    (image, diagram, chart, code)     │
│                                      │
└──────────────────────────────────────┘
```

Instead of: "Benefits of X" followed by bullet points
Use: "X reduces onboarding time by 40%" with a chart showing the data.

### Text Guidelines

| Element | Guideline |
|---------|-----------|
| Title/headline | 1 sentence, max 2 lines |
| Body text | 6 words per line max (when used) |
| Font size | 24pt minimum for body, 32pt+ for titles |
| Font choice | Sans-serif for projection (Inter, Helvetica, Source Sans) |
| Contrast | Dark text on light background or light text on dark |

---

## Slide Type Patterns

### 1. Title Slide

```
┌──────────────────────────────────────┐
│                                      │
│         PRESENTATION TITLE           │
│         Subtitle or tagline          │
│                                      │
│         Your Name                    │
│         Date / Event                 │
│                                      │
└──────────────────────────────────────┘
```

Keep it clean. Title, name, and event — nothing else.

### 2. Section Divider

```
┌──────────────────────────────────────┐
│                                      │
│                                      │
│          01  SECTION NAME            │
│                                      │
│                                      │
└──────────────────────────────────────┘
```

Use a distinct background color or large numbering to signal transitions. These give the audience a mental reset.

### 3. Single Idea Slide

```
┌──────────────────────────────────────┐
│                                      │
│       "One big idea or quote         │
│        in large text."               │
│                                      │
│                        — Attribution │
└──────────────────────────────────────┘
```

Use for emphasis. No more than 10-15 words. Let the words breathe.

### 4. Image + Caption

```
┌──────────────────────────────────────┐
│                                      │
│     ┌────────────────────────┐       │
│     │                        │       │
│     │     Full-width image   │       │
│     │                        │       │
│     └────────────────────────┘       │
│  Brief caption or key point          │
└──────────────────────────────────────┘
```

Image should be high resolution and directly relevant. Caption adds the "so what."

### 5. Comparison / Two-Column

```
┌──────────────────────────────────────┐
│  Headline: Assertion about contrast  │
│                                      │
│   Before       │     After           │
│   ───────      │     ───────         │
│   Point A      │     Point A'        │
│   Point B      │     Point B'        │
│   Point C      │     Point C'        │
│                                      │
└──────────────────────────────────────┘
```

Use for before/after, pros/cons, old/new. Keep both columns balanced.

### 6. Data / Chart Slide

```
┌──────────────────────────────────────┐
│  Headline: What the data shows       │
│                                      │
│     ┌────────────────────────┐       │
│     │                        │       │
│     │   Chart or graph       │       │
│     │   (one data story)     │       │
│     │                        │       │
│     └────────────────────────┘       │
│  Source: [attribution]               │
└──────────────────────────────────────┘
```

Rules for data slides:
- One message per chart
- Headline states the conclusion, not "Q3 Revenue Data"
- Highlight the key data point with color or annotation
- Remove gridlines, excessive labels, 3D effects

### 7. Process / Steps

```
┌──────────────────────────────────────┐
│  How we approach [topic]             │
│                                      │
│   ┌───┐     ┌───┐     ┌───┐        │
│   │ 1 │ ──> │ 2 │ ──> │ 3 │        │
│   └───┘     └───┘     └───┘        │
│  Discover   Define    Deliver       │
│                                      │
└──────────────────────────────────────┘
```

Use progressive disclosure (animate steps appearing one at a time) if presenting live.

### 8. Activity / Exercise Instruction

```
┌──────────────────────────────────────┐
│  ACTIVITY: [Name]         ⏱ 10 min  │
│                                      │
│  1. [First instruction]              │
│  2. [Second instruction]             │
│  3. [Third instruction]              │
│                                      │
│  Deliverable: [What they produce]    │
└──────────────────────────────────────┘
```

Keep instructions visible throughout the activity. Include time and expected output.

### 9. Key Takeaway / Summary

```
┌──────────────────────────────────────┐
│  Key Takeaways                       │
│                                      │
│  1. [First takeaway]                 │
│  2. [Second takeaway]                │
│  3. [Third takeaway]                 │
│                                      │
│  [Optional CTA or resource link]     │
└──────────────────────────────────────┘
```

Three takeaways maximum. If you have more, prioritize or group.

### 10. Closing / Contact Slide

```
┌──────────────────────────────────────┐
│                                      │
│          Thank you.                  │
│                                      │
│          [Your Name]                 │
│          [Email / Website]           │
│          [Social handle]             │
│                                      │
└──────────────────────────────────────┘
```

Leave this slide up during Q&A so people can note your contact information.

---

## Color and Layout

### Choosing a Palette

| Approach | Description |
|----------|-------------|
| Monochromatic | One color in multiple shades — clean, professional |
| Complementary accent | Neutral base + one bold accent color for emphasis |
| Brand-aligned | Use company or event brand colors |

Stick to 2-3 colors total. Use accent color sparingly for emphasis only.

### Consistent Spacing

- Keep margins consistent across all slides (suggest 10-15% of slide width)
- Align elements to a grid
- Use the same position for recurring elements (slide numbers, logos)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Bullet point walls | Replace with visuals or single-idea slides |
| Reading slides aloud | Slides support your talk, they are not the script |
| Tiny text ("I know you can't read this...") | If they can't read it, remove it |
| Inconsistent styling | Use a master template, check before presenting |
| Clip art or stock cliches | Use real photos, diagrams, or no image at all |
| Animations and transitions | Subtle or none — never bouncing, spinning, etc. |
| Too many slides | 1 slide per minute is a good baseline |
| No slide numbers | Add them — helps with Q&A references |

---

## Slide Count Guidelines

| Format | Duration | Slides |
|--------|----------|--------|
| Lightning talk | 5 min | 5-10 |
| Conference talk | 30 min | 25-35 |
| Workshop (teaching) | 2 hours | 30-50 (with activity breaks) |
| Keynote | 45-60 min | 40-60 |

These assume the assertion-evidence style with one idea per slide. Dense bullet-point slides would use fewer slides but are less effective.
