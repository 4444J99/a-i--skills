# WCAG 2.1 Level AA Checklist

Quick reference for meeting Web Content Accessibility Guidelines Level AA.

## Perceivable

### 1.1 Text Alternatives

- [ ] **1.1.1 Non-text Content** (A): All images have alt text
  - Informative images: Describe content/function
  - Decorative images: Empty alt=""
  - Complex images: Brief alt + longer description

### 1.2 Time-based Media

- [ ] **1.2.1 Audio-only/Video-only** (A): Provide alternatives
- [ ] **1.2.2 Captions** (A): Prerecorded video has captions
- [ ] **1.2.3 Audio Description** (A): Video has audio description
- [ ] **1.2.4 Live Captions** (AA): Live video has captions
- [ ] **1.2.5 Audio Description** (AA): Prerecorded video

### 1.3 Adaptable

- [ ] **1.3.1 Info and Relationships** (A): Structure conveyed programmatically
  - Headings marked with h1-h6
  - Lists marked with ul/ol/li
  - Tables have proper headers
  - Form labels associated with inputs
- [ ] **1.3.2 Meaningful Sequence** (A): Reading order makes sense
- [ ] **1.3.3 Sensory Characteristics** (A): Instructions don't rely only on shape/location
- [ ] **1.3.4 Orientation** (AA): Content not locked to portrait/landscape
- [ ] **1.3.5 Input Purpose** (AA): Input fields have autocomplete attributes

### 1.4 Distinguishable

- [ ] **1.4.1 Use of Color** (A): Color not sole indicator
- [ ] **1.4.2 Audio Control** (A): User can pause/stop audio
- [ ] **1.4.3 Contrast (Minimum)** (AA): 4.5:1 for text, 3:1 for large text
- [ ] **1.4.4 Resize Text** (AA): Text resizable to 200% without loss
- [ ] **1.4.5 Images of Text** (AA): Use real text, not images
- [ ] **1.4.10 Reflow** (AA): No horizontal scroll at 320px width
- [ ] **1.4.11 Non-text Contrast** (AA): 3:1 for UI components
- [ ] **1.4.12 Text Spacing** (AA): Content works with modified spacing
- [ ] **1.4.13 Content on Hover/Focus** (AA): Dismissable, hoverable, persistent

## Operable

### 2.1 Keyboard Accessible

- [ ] **2.1.1 Keyboard** (A): All functionality via keyboard
- [ ] **2.1.2 No Keyboard Trap** (A): Focus can move away
- [ ] **2.1.4 Character Key Shortcuts** (A): Can turn off/remap shortcuts

### 2.2 Enough Time

- [ ] **2.2.1 Timing Adjustable** (A): Time limits can be extended
- [ ] **2.2.2 Pause, Stop, Hide** (A): User can control moving content

### 2.3 Seizures

- [ ] **2.3.1 Three Flashes** (A): Nothing flashes >3 times/second

### 2.4 Navigable

- [ ] **2.4.1 Bypass Blocks** (A): Skip to main content link
- [ ] **2.4.2 Page Titled** (A): Descriptive page titles
- [ ] **2.4.3 Focus Order** (A): Logical tab order
- [ ] **2.4.4 Link Purpose (Context)** (A): Link text describes purpose
- [ ] **2.4.5 Multiple Ways** (AA): More than one way to find pages
- [ ] **2.4.6 Headings and Labels** (AA): Descriptive headings/labels
- [ ] **2.4.7 Focus Visible** (AA): Focus indicator visible

### 2.5 Input Modalities

- [ ] **2.5.1 Pointer Gestures** (A): Complex gestures have alternatives
- [ ] **2.5.2 Pointer Cancellation** (A): Actions on up-event
- [ ] **2.5.3 Label in Name** (A): Visible label in accessible name
- [ ] **2.5.4 Motion Actuation** (A): Motion alternatives available

## Understandable

### 3.1 Readable

- [ ] **3.1.1 Language of Page** (A): Lang attribute set
- [ ] **3.1.2 Language of Parts** (AA): Lang changes marked

### 3.2 Predictable

- [ ] **3.2.1 On Focus** (A): Focus doesn't change context
- [ ] **3.2.2 On Input** (A): Input doesn't change context unexpectedly
- [ ] **3.2.3 Consistent Navigation** (AA): Navigation consistent
- [ ] **3.2.4 Consistent Identification** (AA): Same icons/labels throughout

### 3.3 Input Assistance

- [ ] **3.3.1 Error Identification** (A): Errors identified in text
- [ ] **3.3.2 Labels or Instructions** (A): Input fields have labels
- [ ] **3.3.3 Error Suggestion** (AA): Error correction suggested
- [ ] **3.3.4 Error Prevention (Legal)** (AA): Reversible/confirmable submissions

## Robust

### 4.1 Compatible

- [ ] **4.1.1 Parsing** (A): Valid HTML
- [ ] **4.1.2 Name, Role, Value** (A): Custom controls have correct ARIA
- [ ] **4.1.3 Status Messages** (AA): Status messages announced to AT

## Testing Tools

| Tool | Type | Use For |
|------|------|---------|
| axe DevTools | Browser extension | Automated checks |
| WAVE | Browser extension | Visual feedback |
| Lighthouse | Chrome DevTools | Audit report |
| Pa11y | CLI | CI integration |
| VoiceOver | Built-in (macOS) | Screen reader testing |
| NVDA | Free (Windows) | Screen reader testing |
