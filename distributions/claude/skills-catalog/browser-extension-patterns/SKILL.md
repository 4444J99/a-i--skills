---
name: browser-extension-patterns
description: Build browser extensions with Manifest V3 for Chrome, Firefox, and cross-browser compatibility. Covers content scripts, background workers, popup UI, storage APIs, and extension messaging. Triggers on browser extension development, Manifest V3, or Chrome extension requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - browser-extension
  - manifest-v3
  - chrome-extension
  - content-scripts
  - web-extension
governance_phases: [build]
organ_affinity: [organ-iii]
triggers: [user-asks-about-browser-extension, context:chrome-extension, context:manifest-v3, project-has-manifest-json]
complements: [frontend-design-systems, testing-patterns, deployment-cicd]
---

# Browser Extension Patterns

Build cross-browser extensions with Manifest V3 architecture.

## Manifest V3 Structure

```
my-extension/
├── manifest.json          # Extension manifest
├── background/
│   └── service-worker.js  # Background service worker
├── content/
│   └── content-script.js  # Injected into web pages
├── popup/
│   ├── popup.html         # Popup UI
│   ├── popup.js           # Popup logic
│   └── popup.css          # Popup styles
├── options/
│   ├── options.html       # Settings page
│   └── options.js
├── icons/
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
└── _locales/              # Internationalization
    └── en/messages.json
```

### Manifest Configuration

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "Brief description of what it does",
  "permissions": ["storage", "activeTab"],
  "host_permissions": ["https://*.example.com/*"],
  "background": {
    "service_worker": "background/service-worker.js"
  },
  "content_scripts": [{
    "matches": ["https://*.example.com/*"],
    "js": ["content/content-script.js"],
    "css": ["content/content-style.css"],
    "run_at": "document_idle"
  }],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon-16.png",
      "48": "icons/icon-48.png",
      "128": "icons/icon-128.png"
    }
  },
  "options_page": "options/options.html",
  "icons": {
    "16": "icons/icon-16.png",
    "48": "icons/icon-48.png",
    "128": "icons/icon-128.png"
  }
}
```

## Background Service Worker

```javascript
// background/service-worker.js

// Installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    chrome.storage.local.set({ settings: { enabled: true, theme: 'light' } });
  }
});

// Message handling from content scripts and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.type) {
    case 'getData':
      fetchData(message.url).then(sendResponse);
      return true; // Async response
    case 'updateBadge':
      chrome.action.setBadgeText({ text: String(message.count) });
      break;
  }
});

// Alarm-based periodic tasks (replaces MV2 persistent background)
chrome.alarms.create('sync', { periodInMinutes: 30 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'sync') syncData();
});
```

## Content Scripts

```javascript
// content/content-script.js

// DOM manipulation on target pages
function enhancePage() {
  const elements = document.querySelectorAll('.target-class');
  elements.forEach(el => {
    const badge = document.createElement('span');
    badge.className = 'my-extension-badge';
    badge.textContent = 'Enhanced';
    el.appendChild(badge);
  });
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', enhancePage);
} else {
  enhancePage();
}

// Communicate with background
async function requestData(url) {
  return chrome.runtime.sendMessage({ type: 'getData', url });
}

// Listen for messages from background/popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'getPageData') {
    sendResponse({ title: document.title, url: location.href });
  }
});
```

## Storage Patterns

```javascript
// Chrome storage API (synced across devices)
const storage = {
  async get(key) {
    const result = await chrome.storage.sync.get(key);
    return result[key];
  },

  async set(key, value) {
    await chrome.storage.sync.set({ [key]: value });
  },

  async getLocal(key) {
    const result = await chrome.storage.local.get(key);
    return result[key];
  },

  onChange(callback) {
    chrome.storage.onChanged.addListener((changes, area) => {
      callback(changes, area);
    });
  }
};

// Usage
await storage.set('settings', { theme: 'dark', enabled: true });
const settings = await storage.get('settings');
```

## Popup UI

```html
<!-- popup/popup.html -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div id="app">
    <h2>My Extension</h2>
    <label>
      <input type="checkbox" id="enabled"> Enabled
    </label>
    <div id="status"></div>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

```javascript
// popup/popup.js
document.addEventListener('DOMContentLoaded', async () => {
  const settings = await chrome.storage.sync.get('settings');
  document.getElementById('enabled').checked = settings.settings?.enabled;

  document.getElementById('enabled').addEventListener('change', async (e) => {
    await chrome.storage.sync.set({
      settings: { ...settings.settings, enabled: e.target.checked }
    });
    // Notify content scripts
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, { type: 'settingsChanged', enabled: e.target.checked });
  });
});
```

## Cross-Browser Compatibility

```javascript
// Polyfill for Firefox WebExtensions API
const browser = globalThis.browser || globalThis.chrome;

// Feature detection
const isFirefox = typeof browser !== 'undefined' && browser.runtime?.getBrowserInfo;
const isChrome = typeof chrome !== 'undefined' && chrome.runtime?.id;
```

### Firefox Manifest Differences

```json
{
  "background": {
    "scripts": ["background/service-worker.js"]
  },
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.com",
      "strict_min_version": "109.0"
    }
  }
}
```

## Permission Strategy

| Permission | When | Impact |
|-----------|------|--------|
| `activeTab` | Need current tab only | Low (user-triggered) |
| `storage` | Need to save settings | Low |
| `tabs` | Need tab URLs/titles | Medium |
| `host_permissions` | Need page access | High (shows warning) |
| `<all_urls>` | Need all page access | Very High (avoid if possible) |

**Principle:** Request minimum permissions. Use `activeTab` over broad host permissions when possible.

## Anti-Patterns

- **MV2 patterns in MV3** — No persistent background pages; use service workers and alarms
- **`<all_urls>` permission** — Request only the hosts you need
- **Synchronous storage** — Always use async `chrome.storage` API
- **No error handling in messaging** — Messages fail silently if receiver doesn't exist
- **Heavy content scripts** — Minimize injected code; communicate with background for heavy work
- **No uninstall cleanup** — Use `runtime.onInstalled` to handle updates and cleanup
