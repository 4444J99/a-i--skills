# Common ARIA Patterns

Reusable ARIA implementations for interactive UI components. Follow the WAI-ARIA Authoring Practices.

## Rule of ARIA

1. Use native HTML elements first (`<button>`, `<select>`, `<input>`)
2. Do not change native semantics unless necessary
3. All interactive ARIA controls must be keyboard operable
4. Do not use `role="presentation"` or `aria-hidden="true"` on focusable elements
5. All interactive elements must have an accessible name

## Disclosure (Show/Hide)

```html
<button aria-expanded="false" aria-controls="content-1">
  Show details
</button>
<div id="content-1" hidden>
  <p>Additional content revealed on click.</p>
</div>

<script>
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!expanded));
    content.hidden = expanded;
  });
</script>
```

**Keyboard**: Enter or Space toggles.

## Accordion

```html
<div role="region" aria-labelledby="accordion-header-1">
  <h3>
    <button id="accordion-header-1"
            aria-expanded="true"
            aria-controls="accordion-panel-1">
      Section One
    </button>
  </h3>
  <div id="accordion-panel-1" role="region" aria-labelledby="accordion-header-1">
    <p>Panel content...</p>
  </div>
</div>
```

**Keyboard**: Arrow keys move between headers; Enter/Space toggles panel.

## Tabs

```html
<div role="tablist" aria-label="Project settings">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">General</button>
  <button role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2" tabindex="-1">Security</button>
  <button role="tab" id="tab-3" aria-selected="false" aria-controls="panel-3" tabindex="-1">Billing</button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">General content</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>Security content</div>
<div role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>Billing content</div>
```

| Key | Action |
|-----|--------|
| Left/Right Arrow | Move between tabs |
| Home | First tab |
| End | Last tab |
| Enter/Space | Activate tab (if manual activation) |

## Modal Dialog

```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Delete Item</h2>
  <p id="dialog-desc">This action cannot be undone. Continue?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

**Focus management**:

1. On open: move focus to first focusable element (or the dialog itself)
2. Trap focus: Tab and Shift+Tab cycle within the dialog only
3. On close: return focus to the element that triggered the dialog
4. Escape key closes the dialog

## Alert and Status Messages

```html
<!-- Assertive: interrupts screen reader -->
<div role="alert">Error: Your session has expired.</div>

<!-- Polite: announced after current speech -->
<div role="status">3 results found.</div>

<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true">
  Cart total: $42.00
</div>
```

| Attribute | Values | Effect |
|-----------|--------|--------|
| `aria-live` | `polite`, `assertive`, `off` | When to announce |
| `aria-atomic` | `true`, `false` | Announce whole region or just change |
| `aria-relevant` | `additions`, `removals`, `text`, `all` | What changes to announce |

## Menu and Menubar

```html
<button aria-haspopup="true" aria-expanded="false" aria-controls="file-menu">File</button>
<ul role="menu" id="file-menu" hidden>
  <li role="menuitem">New</li>
  <li role="menuitem">Open</li>
  <li role="separator"></li>
  <li role="menuitem">Save</li>
</ul>
```

| Key | Action |
|-----|--------|
| Enter/Space | Open menu or activate item |
| Arrow Down | Next item |
| Arrow Up | Previous item |
| Escape | Close menu, return focus to button |
| Home/End | First/last item |

## Tooltip

```html
<button aria-describedby="tooltip-1">Settings</button>
<div role="tooltip" id="tooltip-1">Configure application preferences</div>
```

- Tooltip appears on hover and focus
- Disappears on Escape, mouse leave, or blur
- Should not contain interactive elements

## Combobox (Autocomplete)

```html
<label for="city-input">City</label>
<input id="city-input"
       role="combobox"
       aria-expanded="false"
       aria-autocomplete="list"
       aria-controls="city-listbox"
       aria-activedescendant="">
<ul role="listbox" id="city-listbox" hidden>
  <li role="option" id="city-1">Austin</li>
  <li role="option" id="city-2">Boston</li>
</ul>
```

Set `aria-activedescendant` to the `id` of the highlighted option as the user arrows through the list.

## Breadcrumb

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/shoes" aria-current="page">Shoes</a></li>
  </ol>
</nav>
```

Use `aria-current="page"` on the last link to indicate the current page.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding `role="button"` to `<div>` without keyboard handling | Use `<button>` or add `tabindex="0"` + Enter/Space handlers |
| Using `aria-label` and visible text that differ | Keep them consistent; use `aria-labelledby` when visible text exists |
| Hiding content with `display:none` but expecting AT to read it | Use `aria-live` or visually-hidden class instead |
| Using `aria-hidden="true"` on a parent of focusable elements | Remove from tab order first with `tabindex="-1"` |
| Redundant roles on semantic elements (e.g., `<nav role="navigation">`) | Omit the role; native semantics are sufficient |
