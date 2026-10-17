# Root Hygiene Checklist

Audit checklist for implementing the Minimal Root philosophy.

---

## Quick Audit

Run this assessment on your repository root:

```bash
ls -la | wc -l
```

| Count | Assessment |
|-------|------------|
| < 15 | Excellent - minimal root |
| 15-25 | Acceptable - review for opportunities |
| 25-40 | Cluttered - needs organization |
| > 40 | Critical - significant cleanup needed |

---

## Root Directory Audit

### Allowed in Root

These items belong in the root directory:

- [ ] `README.md` - Primary documentation entry point
- [ ] `LICENSE` - Required for open source
- [ ] `CHANGELOG.md` - Version history (optional, can be in docs/)
- [ ] `.gitignore` - Git ignore patterns
- [ ] `.gitattributes` - Git attributes (optional)
- [ ] `package.json` / `Cargo.toml` / `pyproject.toml` - Primary manifest
- [ ] `tsconfig.json` - Only if needed at root for IDE support

### Directories Allowed in Root

- [ ] `src/` or `lib/` - Source code
- [ ] `docs/` - Extended documentation
- [ ] `tests/` or `test/` - Test files (if not colocated)
- [ ] `scripts/` or `tools/` - Build/dev scripts
- [ ] `.github/` - GitHub-specific files
- [ ] `.config/` - Centralized tool configs

---

## Files to Relocate

### Move to `.config/`

| File | New Location | Tool Config |
|------|-------------|-------------|
| `.eslintrc.*` | `.config/eslint.config.js` | `ESLINT_USE_FLAT_CONFIG=true` |
| `.prettierrc.*` | `.config/prettier.config.js` | `--config .config/prettier.config.js` |
| `.stylelintrc.*` | `.config/stylelint.config.js` | `--config .config/stylelint.config.js` |
| `jest.config.*` | `.config/jest.config.js` | `--config .config/jest.config.js` |
| `vitest.config.*` | `.config/vitest.config.js` | `--config .config/vitest.config.js` |
| `.babelrc` | `.config/babel.config.js` | Babel auto-detects |
| `tailwind.config.*` | `.config/tailwind.config.js` | `--config .config/tailwind.config.js` |
| `postcss.config.*` | `.config/postcss.config.js` | PostCSS auto-detects |
| `.env.example` | `.config/.env.example` | Copy to root as `.env` |

### Move to `.github/`

| File | New Location |
|------|-------------|
| `CONTRIBUTING.md` | `.github/CONTRIBUTING.md` |
| `CODE_OF_CONDUCT.md` | `.github/CODE_OF_CONDUCT.md` |
| `SECURITY.md` | `.github/SECURITY.md` |
| `SUPPORT.md` | `.github/SUPPORT.md` |
| `CODEOWNERS` | `.github/CODEOWNERS` |
| `FUNDING.yml` | `.github/FUNDING.yml` |
| `PULL_REQUEST_TEMPLATE.md` | `.github/PULL_REQUEST_TEMPLATE.md` |
| `ISSUE_TEMPLATE/` | `.github/ISSUE_TEMPLATE/` |

### Move to `docs/`

| File | New Location |
|------|-------------|
| `ARCHITECTURE.md` | `docs/ARCHITECTURE.md` |
| `API.md` | `docs/API.md` |
| `DEPLOYMENT.md` | `docs/DEPLOYMENT.md` |
| `*.md` (non-essential) | `docs/[name].md` |
| `images/` | `docs/images/` |
| `diagrams/` | `docs/diagrams/` |

### Files That Stay in Root

These cannot be moved (tool constraints):

- `package.json` - npm requires root
- `package-lock.json` - npm requires root
- `tsconfig.json` - IDE support often requires root
- `.gitignore` - Git requires root
- `.npmrc` - npm requires root
- `.nvmrc` - nvm requires root
- `Dockerfile` - Docker default expects root

---

## Tool Configuration Updates

### ESLint (Flat Config)

```javascript
// .config/eslint.config.js
export default [
  {
    // Your config here
  }
];
```

```json
// package.json
{
  "scripts": {
    "lint": "ESLINT_USE_FLAT_CONFIG=true eslint . --config .config/eslint.config.js"
  }
}
```

### Prettier

```javascript
// .config/prettier.config.js
export default {
  semi: true,
  singleQuote: true,
  // ...
};
```

```json
// package.json
{
  "scripts": {
    "format": "prettier --config .config/prettier.config.js --write ."
  }
}
```

### Jest

```javascript
// .config/jest.config.js
export default {
  rootDir: '..',
  testMatch: ['<rootDir>/tests/**/*.test.js'],
  // ...
};
```

```json
// package.json
{
  "scripts": {
    "test": "jest --config .config/jest.config.js"
  }
}
```

### Tailwind CSS

```javascript
// .config/tailwind.config.js
export default {
  content: ['../src/**/*.{js,ts,jsx,tsx}'],
  // ...
};
```

```json
// package.json
{
  "scripts": {
    "build:css": "tailwindcss -c .config/tailwind.config.js -o dist/styles.css"
  }
}
```

---

## VS Code Integration

Update `.vscode/settings.json` to point to new locations:

```json
{
  "eslint.options": {
    "overrideConfigFile": ".config/eslint.config.js"
  },
  "prettier.configPath": ".config/prettier.config.js",
  "stylelint.configFile": ".config/stylelint.config.js"
}
```

---

## Final Audit Checklist

After cleanup, verify:

### Root Directory

- [ ] Only essential files remain
- [ ] No orphaned config files
- [ ] Clear purpose for every item
- [ ] `.config/` contains tool configs
- [ ] `docs/` contains documentation

### Functionality

- [ ] `npm run lint` works
- [ ] `npm run format` works
- [ ] `npm run test` works
- [ ] `npm run build` works
- [ ] IDE integrations work (formatting, linting)
- [ ] CI/CD pipelines work

### Documentation

- [ ] README updated with new structure
- [ ] Contributing guide updated (if moved)
- [ ] Development setup instructions accurate

---

## Common Issues

### Issue: Tool can't find config

**Symptom:** "Config file not found" errors

**Fix:** Ensure CLI flag points to new location OR update tool's config resolution setting.

### Issue: IDE not respecting config

**Symptom:** Different behavior in IDE vs CLI

**Fix:** Update `.vscode/settings.json` or equivalent IDE config.

### Issue: CI failing after move

**Symptom:** CI worked locally but fails remotely

**Fix:** Update CI workflow files to pass config paths explicitly.

### Issue: Pre-commit hooks broken

**Symptom:** Husky/lint-staged not finding configs

**Fix:** Update `.husky/` scripts and lint-staged config to reference new paths.

---

## Verification Commands

```bash
# Check root item count
ls -la | wc -l

# Verify ESLint config resolution
npx eslint --print-config src/index.js

# Verify Prettier config resolution
npx prettier --find-config-path src/index.js

# Test all scripts
npm run lint && npm run format && npm run test && npm run build
```
