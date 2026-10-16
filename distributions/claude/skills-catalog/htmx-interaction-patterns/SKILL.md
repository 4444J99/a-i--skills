---
name: htmx-interaction-patterns
description: Build dynamic web interfaces with htmx using hypermedia-driven patterns for partial page updates, lazy loading, infinite scroll, and server-sent events without writing JavaScript. Triggers on htmx usage, hypermedia architecture, or progressive enhancement requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - htmx
  - hypermedia
  - progressive-enhancement
  - server-side-rendering
governance_phases: [build]
organ_affinity: [meta]
triggers: [user-asks-about-htmx, project-has-htmx, context:hypermedia, context:progressive-enhancement]
complements: [fastapi-patterns, backend-implementation-patterns, responsive-design-patterns]
---

# htmx Interaction Patterns

Build dynamic interfaces with HTML-over-the-wire — server renders HTML fragments, htmx swaps them in.

## Core Concepts

htmx extends HTML with attributes that make AJAX requests and swap content — no JavaScript required.

```html
<!-- Click button → GET /items → replace #item-list content -->
<button hx-get="/items" hx-target="#item-list" hx-swap="innerHTML">
  Load Items
</button>
<div id="item-list"></div>
```

### Key Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `hx-get` | GET request | `hx-get="/api/items"` |
| `hx-post` | POST request | `hx-post="/api/items"` |
| `hx-put` | PUT request | `hx-put="/api/items/1"` |
| `hx-delete` | DELETE request | `hx-delete="/api/items/1"` |
| `hx-target` | Where to put response | `hx-target="#results"` |
| `hx-swap` | How to insert | `hx-swap="outerHTML"` |
| `hx-trigger` | When to fire | `hx-trigger="click"` |
| `hx-indicator` | Loading indicator | `hx-indicator="#spinner"` |

### Swap Strategies

| Strategy | Behavior |
|----------|----------|
| `innerHTML` | Replace children (default) |
| `outerHTML` | Replace entire target element |
| `afterbegin` | Insert as first child |
| `beforeend` | Insert as last child |
| `beforebegin` | Insert before target |
| `afterend` | Insert after target |
| `delete` | Remove target |
| `none` | No DOM update |

## Common Patterns

### Search with Debounce

```html
<input type="search" name="q"
  hx-get="/search"
  hx-trigger="input changed delay:300ms"
  hx-target="#results"
  hx-indicator="#search-spinner"
  placeholder="Search skills...">
<span id="search-spinner" class="htmx-indicator">Searching...</span>
<div id="results"></div>
```

Server returns an HTML fragment:
```python
@app.get("/search")
async def search(q: str = ""):
    results = search_skills(q)
    return HTMLResponse(render_results(results))
```

### Inline Editing

```html
<!-- View mode -->
<div id="skill-42" hx-get="/skills/42/edit" hx-trigger="dblclick" hx-swap="outerHTML">
  <h3>testing-patterns</h3>
  <p>Write effective tests across the stack...</p>
</div>

<!-- Edit mode (returned by server) -->
<form id="skill-42" hx-put="/skills/42" hx-swap="outerHTML">
  <input name="name" value="testing-patterns">
  <textarea name="description">Write effective tests...</textarea>
  <button type="submit">Save</button>
  <button hx-get="/skills/42" hx-swap="outerHTML">Cancel</button>
</form>
```

### Infinite Scroll

```html
<div id="item-list">
  <!-- Items rendered here -->
  <div hx-get="/items?page=2"
       hx-trigger="revealed"
       hx-swap="outerHTML">
    Loading more...
  </div>
</div>
```

Server returns items + next trigger:
```html
<div class="item">Item 11</div>
<div class="item">Item 12</div>
<!-- Next page trigger -->
<div hx-get="/items?page=3" hx-trigger="revealed" hx-swap="outerHTML">
  Loading more...
</div>
```

### Lazy Loading

```html
<div hx-get="/dashboard/metrics" hx-trigger="load" hx-swap="innerHTML">
  <div class="skeleton-loader"></div>
</div>
```

### Active Search with URL State

```html
<input type="search" name="q"
  hx-get="/search"
  hx-trigger="input changed delay:300ms"
  hx-target="#results"
  hx-push-url="true">
```

### Confirmation Dialogs

```html
<button hx-delete="/items/42"
        hx-confirm="Delete this item?"
        hx-target="#item-42"
        hx-swap="outerHTML swap:500ms">
  Delete
</button>
```

### Server-Sent Events

```html
<div hx-ext="sse" sse-connect="/events" sse-swap="message">
  Waiting for updates...
</div>
```

```python
from sse_starlette.sse import EventSourceResponse

@app.get("/events")
async def events():
    async def generate():
        while True:
            data = await get_update()
            yield {"data": render_update(data)}
    return EventSourceResponse(generate())
```

## Server-Side Patterns

### Partial vs Full Responses

```python
@app.get("/items")
async def list_items(request: Request):
    items = await get_items()
    if "HX-Request" in request.headers:
        # htmx request: return fragment
        return HTMLResponse(render_items_fragment(items))
    else:
        # Normal request: return full page
        return HTMLResponse(render_full_page(items))
```

### Response Headers

```python
from starlette.responses import HTMLResponse

@app.post("/items")
async def create_item(request: Request):
    item = await save_item(request)
    response = HTMLResponse(render_item(item))
    response.headers["HX-Trigger"] = "itemCreated"  # Client-side event
    response.headers["HX-Retarget"] = "#item-list"
    response.headers["HX-Reswap"] = "afterbegin"
    return response
```

### OOB (Out-of-Band) Swaps

Update multiple elements from one response:

```html
<!-- Primary swap -->
<div id="item-42">Updated item content</div>
<!-- OOB: also update the counter -->
<span id="item-count" hx-swap-oob="true">43 items</span>
```

## CSS Integration

```css
/* Loading indicator */
.htmx-indicator { opacity: 0; transition: opacity 200ms; }
.htmx-request .htmx-indicator { opacity: 1; }

/* Settling animation */
.htmx-settling { opacity: 0; }
.htmx-settled { opacity: 1; transition: opacity 300ms; }

/* Added items */
.htmx-added { opacity: 0; }
.htmx-settled.htmx-added { opacity: 1; transition: opacity 300ms; }
```

## Anti-Patterns

- **Returning JSON from htmx endpoints** — Always return rendered HTML fragments
- **Large page replacements** — Return small, targeted fragments
- **No loading indicators** — Always show feedback during requests
- **Ignoring non-htmx requests** — Support full-page loads for bookmarkability
- **Client-side state management** — Keep state on the server; let HTML be the state
