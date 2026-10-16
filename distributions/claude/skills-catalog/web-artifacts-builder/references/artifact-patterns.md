# Web Artifacts Patterns

Patterns for building self-contained web artifacts.

## Single-File HTML Artifacts

### Basic Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Artifact Title</title>
  <style>
    /* All CSS inline */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; }
  </style>
</head>
<body>
  <div id="app"></div>

  <script>
    // All JavaScript inline
    const app = document.getElementById('app');
    // Application code...
  </script>
</body>
</html>
```

### With External CDN Dependencies

```html
<!DOCTYPE html>
<html>
<head>
  <!-- CDN libraries -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div id="root"></div>

  <script>
    const { useState } = React;

    function App() {
      const [count, setCount] = useState(0);
      return React.createElement('div', { className: 'p-4' },
        React.createElement('button', {
          onClick: () => setCount(c => c + 1),
          className: 'bg-blue-500 text-white px-4 py-2 rounded'
        }, `Count: ${count}`)
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(
      React.createElement(App)
    );
  </script>
</body>
</html>
```

## Interactive Patterns

### State Management

```javascript
// Simple state management for artifacts
const state = {
  data: [],
  loading: false,
  error: null
};

function setState(updates) {
  Object.assign(state, updates);
  render();
}

function render() {
  const app = document.getElementById('app');
  app.innerHTML = `
    ${state.loading ? '<div class="loading">Loading...</div>' : ''}
    ${state.error ? `<div class="error">${state.error}</div>` : ''}
    <ul>
      ${state.data.map(item => `<li>${item.name}</li>`).join('')}
    </ul>
  `;
}
```

### Event Handling

```javascript
// Event delegation for dynamic content
document.getElementById('app').addEventListener('click', (e) => {
  if (e.target.matches('.delete-btn')) {
    const id = e.target.dataset.id;
    deleteItem(id);
  }

  if (e.target.matches('.edit-btn')) {
    const id = e.target.dataset.id;
    editItem(id);
  }
});
```

### Form Handling

```javascript
function handleForm(formId, onSubmit) {
  const form = document.getElementById(formId);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    onSubmit(data);
  });
}

// Usage
handleForm('user-form', (data) => {
  console.log('Form submitted:', data);
  addUser(data);
  form.reset();
});
```

## Visualization Patterns

### Canvas Drawing

```javascript
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// High DPI support
const dpr = window.devicePixelRatio || 1;
canvas.width = canvas.clientWidth * dpr;
canvas.height = canvas.clientHeight * dpr;
ctx.scale(dpr, dpr);

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Drawing code...
  requestAnimationFrame(draw);
}

draw();
```

### SVG Generation

```javascript
function createSVG(width, height) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.setAttribute('width', width);
  svg.setAttribute('height', height);
  return svg;
}

function circle(cx, cy, r, fill) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  el.setAttribute('cx', cx);
  el.setAttribute('cy', cy);
  el.setAttribute('r', r);
  el.setAttribute('fill', fill);
  return el;
}

// Usage
const svg = createSVG(400, 400);
svg.appendChild(circle(200, 200, 50, '#3b82f6'));
document.body.appendChild(svg);
```

## Data Patterns

### Local Storage Persistence

```javascript
const STORAGE_KEY = 'artifact-data';

function loadData() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
}

function saveData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}
```

### URL State

```javascript
// Store state in URL hash
function getStateFromURL() {
  try {
    const hash = window.location.hash.slice(1);
    return hash ? JSON.parse(decodeURIComponent(hash)) : {};
  } catch {
    return {};
  }
}

function setStateInURL(state) {
  const hash = encodeURIComponent(JSON.stringify(state));
  window.location.hash = hash;
}

// React to URL changes
window.addEventListener('hashchange', () => {
  const state = getStateFromURL();
  render(state);
});
```

## Styling Patterns

### CSS Custom Properties Theme

```html
<style>
:root {
  --primary: #3b82f6;
  --secondary: #64748b;
  --background: #ffffff;
  --foreground: #1e293b;
  --border: #e2e8f0;
  --radius: 0.5rem;
}

.dark {
  --primary: #60a5fa;
  --background: #0f172a;
  --foreground: #f1f5f9;
  --border: #334155;
}

button {
  background: var(--primary);
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
}

.card {
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem;
}
</style>
```

### Minimal Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
}

body {
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}
```

## Deployment Patterns

### Data URI Images

```html
<!-- Embed small images as base64 -->
<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0..." alt="Icon">
```

### Self-Contained Fonts

```css
@font-face {
  font-family: 'CustomFont';
  src: url(data:font/woff2;base64,...) format('woff2');
}
```

### No External Dependencies

Prefer:
- Inline CSS over external stylesheets
- Inline JavaScript over external scripts
- Data URIs over external images
- System fonts over web fonts

## Best Practices

1. **Keep it small**: Target <100KB uncompressed
2. **Test offline**: Should work without network
3. **Mobile-first**: Ensure touch support
4. **Accessible**: Include ARIA labels
5. **Performant**: Use requestAnimationFrame for animations
6. **Shareable**: Works when copy-pasted
