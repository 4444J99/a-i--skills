# Responsive Design Patterns

Breakpoints, layouts, and responsive techniques.

## Standard Breakpoints

### Tailwind CSS Defaults

| Breakpoint | Min Width | Target Devices |
|------------|-----------|----------------|
| `sm` | 640px | Large phones (landscape) |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large screens |

### Bootstrap 5

| Breakpoint | Min Width |
|------------|-----------|
| `xs` | 0 |
| `sm` | 576px |
| `md` | 768px |
| `lg` | 992px |
| `xl` | 1200px |
| `xxl` | 1400px |

### Custom CSS

```css
/* Mobile-first approach */
.container { width: 100%; }

@media (min-width: 640px) { .container { max-width: 640px; } }
@media (min-width: 768px) { .container { max-width: 768px; } }
@media (min-width: 1024px) { .container { max-width: 1024px; } }
@media (min-width: 1280px) { .container { max-width: 1280px; } }
```

## Layout Patterns

### Holy Grail Layout

```css
.layout {
  display: grid;
  grid-template:
    "header header header" auto
    "nav    main   aside" 1fr
    "footer footer footer" auto
    / 200px 1fr 200px;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .layout {
    grid-template:
      "header" auto
      "nav" auto
      "main" 1fr
      "aside" auto
      "footer" auto
      / 1fr;
  }
}
```

### Card Grid

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}
```

### Sidebar Layout

```css
.sidebar-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
}

@media (max-width: 768px) {
  .sidebar-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: fixed;
    transform: translateX(-100%);
    transition: transform 0.3s;
  }

  .sidebar.open {
    transform: translateX(0);
  }
}
```

## Responsive Typography

### Fluid Typography

```css
/* Scales between 16px at 320px and 24px at 1200px */
html {
  font-size: clamp(1rem, 0.5rem + 2vw, 1.5rem);
}

/* Heading scale */
h1 { font-size: clamp(2rem, 1.5rem + 2vw, 3rem); }
h2 { font-size: clamp(1.5rem, 1.25rem + 1.5vw, 2.25rem); }
h3 { font-size: clamp(1.25rem, 1rem + 1vw, 1.75rem); }
```

### Type Scale

| Element | Mobile | Desktop |
|---------|--------|---------|
| Body | 16px | 18px |
| H1 | 32px | 48px |
| H2 | 24px | 36px |
| H3 | 20px | 28px |
| Small | 14px | 14px |

## Responsive Images

### srcset and sizes

```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="
    (max-width: 400px) 100vw,
    (max-width: 800px) 80vw,
    800px
  "
  alt="Description"
>
```

### Picture Element

```html
<picture>
  <source
    media="(min-width: 1024px)"
    srcset="hero-desktop.jpg"
  >
  <source
    media="(min-width: 768px)"
    srcset="hero-tablet.jpg"
  >
  <img src="hero-mobile.jpg" alt="Hero">
</picture>
```

### CSS Object Fit

```css
.image-container {
  aspect-ratio: 16 / 9;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* or contain */
}
```

## Navigation Patterns

### Hamburger Menu

```css
.nav-toggle {
  display: none;
}

.nav-menu {
  display: flex;
  gap: 1rem;
}

@media (max-width: 768px) {
  .nav-toggle {
    display: block;
  }

  .nav-menu {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: 1rem;
    display: none;
  }

  .nav-menu.open {
    display: flex;
  }
}
```

### Priority+ Navigation

Show important items, collapse rest into "More" menu.

```css
.nav {
  display: flex;
  overflow: hidden;
}

.nav-item {
  flex-shrink: 0;
}

.nav-more {
  margin-left: auto;
}
```

## Container Queries

```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query container */
@container card (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
}

@container card (max-width: 399px) {
  .card {
    flex-direction: column;
  }
}
```

## Spacing Patterns

### Responsive Spacing

```css
:root {
  --space-sm: clamp(0.5rem, 1vw, 1rem);
  --space-md: clamp(1rem, 2vw, 2rem);
  --space-lg: clamp(2rem, 4vw, 4rem);
}

.section {
  padding: var(--space-lg) var(--space-md);
}
```

### Stack Spacing

```css
.stack > * + * {
  margin-top: var(--stack-space, 1.5rem);
}

.stack--sm { --stack-space: 0.75rem; }
.stack--lg { --stack-space: 3rem; }
```

## Testing Checklist

- [ ] Test at each breakpoint
- [ ] Test between breakpoints (resize smoothly)
- [ ] Test landscape orientation
- [ ] Test with zoom (200%)
- [ ] Test with different font sizes
- [ ] Test touch targets (44px minimum)
- [ ] Test text readability (line length 45-75 characters)
- [ ] Test on actual devices
