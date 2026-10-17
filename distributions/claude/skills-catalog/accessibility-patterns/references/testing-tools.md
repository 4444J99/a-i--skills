# Accessibility Testing Tool Setup

Configuration and usage for automated and manual accessibility testing tools.

## Automated Testing in CI

### axe-core with Vitest

```bash
npm install -D @axe-core/react vitest axe-core
```

```typescript
// test/setup.ts
import 'vitest-axe/extend-expect';
```

```typescript
// components/Button.test.tsx
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';

it('should have no a11y violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### jest-axe (if using Jest)

```bash
npm install -D jest-axe @types/jest-axe
```

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('form should be accessible', async () => {
  const { container } = render(<LoginForm />);
  expect(await axe(container)).toHaveNoViolations();
});
```

### Playwright Accessibility Testing

```bash
npm install -D @axe-core/playwright
```

```typescript
// e2e/a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('homepage should pass axe audit', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});

// Scan specific region
test('navigation should be accessible', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .include('nav')
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### Pa11y in CI Pipeline

```bash
npm install -D pa11y pa11y-ci
```

```json
// .pa11yci
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 10000,
    "wait": 1000
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/login",
    "http://localhost:3000/dashboard"
  ]
}
```

```yaml
# GitHub Actions
- name: Accessibility audit
  run: |
    npm start &
    npx wait-on http://localhost:3000
    npx pa11y-ci
```

## Browser Extensions

### axe DevTools

| Feature | How |
|---------|-----|
| Install | Chrome Web Store or Firefox Add-ons |
| Run scan | DevTools > axe DevTools tab > Scan |
| Filter | By severity, WCAG level, or rule |
| Highlight | Click issue to see element on page |

Best for: Comprehensive automated checks during development.

### WAVE (Web Accessibility Evaluation)

| Feature | How |
|---------|-----|
| Install | Chrome Web Store or Firefox Add-ons |
| Run scan | Click WAVE icon in toolbar |
| View | Inline icons show issues directly on page |
| Structure | Tab shows heading/landmark outline |

Best for: Visual feedback and structural overview.

### Lighthouse (Built into Chrome)

```
DevTools > Lighthouse tab > Check "Accessibility" > Generate report
```

- Scores 0-100 based on axe-core rules
- Covers a subset of WCAG criteria
- Good for quick audits, not comprehensive

## Screen Reader Testing

### VoiceOver (macOS)

| Action | Shortcut |
|--------|----------|
| Toggle on/off | Cmd + F5 |
| Read next item | VO + Right Arrow (VO = Ctrl + Option) |
| Interact with group | VO + Shift + Down Arrow |
| Stop interaction | VO + Shift + Up Arrow |
| Open rotor (landmarks, headings) | VO + U |
| Read page from top | VO + A |

Test in **Safari** for best compatibility.

### NVDA (Windows, Free)

| Action | Shortcut |
|--------|----------|
| Toggle on/off | Ctrl + Alt + N |
| Read next item | Down Arrow |
| List headings | NVDA + F7 |
| List landmarks | NVDA + F7, switch to landmarks |
| Stop reading | Ctrl |

Test in **Firefox** for best compatibility.

### TalkBack (Android)

| Action | Gesture |
|--------|---------|
| Read next | Swipe right |
| Read previous | Swipe left |
| Activate | Double tap |
| Scroll | Two-finger swipe |

## Color Contrast Checking

### CLI: color-contrast-checker

```bash
npx color-contrast-checker "#333333" "#ffffff"
# Output: Ratio 12.63:1 — PASS AA, PASS AAA
```

### Programmatic Check

```typescript
// Using polished
import { meetsContrastGuidelines } from 'polished';

const result = meetsContrastGuidelines('#333', '#fff');
// { AA: true, AALarge: true, AAA: true, AAALarge: true }
```

### Chrome DevTools

1. Inspect an element
2. Click the color swatch next to a `color` property
3. The contrast ratio is shown with AA/AAA pass/fail indicators

## ESLint Plugin

```bash
npm install -D eslint-plugin-jsx-a11y
```

```json
// .eslintrc.json
{
  "extends": ["plugin:jsx-a11y/recommended"],
  "plugins": ["jsx-a11y"]
}
```

Key rules caught at lint time:

| Rule | Catches |
|------|---------|
| `alt-text` | Missing alt on images |
| `anchor-is-valid` | Empty or invalid href |
| `click-events-have-key-events` | onClick without onKeyDown |
| `no-noninteractive-element-interactions` | Click on `<div>` |
| `label-has-associated-control` | Orphaned labels |

## Recommended Testing Workflow

1. **Lint** (ESLint jsx-a11y) -- catches issues at write time
2. **Unit tests** (axe-core) -- validates component accessibility
3. **E2E tests** (Playwright + axe) -- validates page-level compliance
4. **CI audit** (Pa11y or Lighthouse CI) -- gates PRs on accessibility score
5. **Manual** (screen reader + keyboard) -- catches what automation misses

Target: Automate 50-60% of WCAG checks; manual testing covers the rest.
