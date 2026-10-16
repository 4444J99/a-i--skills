# Configuration Migration Recipes

Practical recipes for relocating configuration files from root to `.config/` while maintaining tool functionality.

## The .config/ Strategy

The `.config/` directory centralizes all mutable tool configurations, mimicking the XDG Base Directory specification (`~/.config/`) at the project level.

### Goals

1. **Root clarity** - Only architectural pillars visible at root
2. **Config discoverability** - All configs in one predictable location
3. **Tool compatibility** - Glue code ensures tools still work

## Migration Recipes

### ESLint (v9+ Flat Config)

**Source:** Root `.eslintrc.js` or `eslint.config.js`
**Target:** `.config/eslint.config.js`

**package.json script:**
```json
{
  "scripts": {
    "lint": "eslint . --config .config/eslint.config.js",
    "lint:fix": "eslint . --config .config/eslint.config.js --fix"
  }
}
```

**VS Code settings (.vscode/settings.json):**
```json
{
  "eslint.options": {
    "overrideConfigFile": ".config/eslint.config.js"
  },
  "eslint.workingDirectories": [{ "mode": "auto" }]
}
```

**Notes:**
- ESLint v9+ uses flat config by default
- Legacy `.eslintrc.*` formats still supported with `--config` flag
- The `--config` flag overrides automatic config discovery

---

### Prettier

**Source:** Root `.prettierrc` or `prettier.config.js`
**Target:** `.config/.prettierrc.json`

**package.json script:**
```json
{
  "scripts": {
    "format": "prettier --config .config/.prettierrc.json --write .",
    "format:check": "prettier --config .config/.prettierrc.json --check ."
  }
}
```

**VS Code settings:**
```json
{
  "prettier.configPath": ".config/.prettierrc.json"
}
```

**Notes:**
- Prettier searches up directory tree by default
- The `configPath` setting is essential for editor integration
- Ignore file (`.prettierignore`) can stay in root or move to `.config/`

---

### Stylelint

**Source:** Root `.stylelintrc`
**Target:** `.config/stylelint.config.js`

**package.json script:**
```json
{
  "scripts": {
    "lint:css": "stylelint '**/*.css' --config .config/stylelint.config.js"
  }
}
```

**VS Code settings:**
```json
{
  "stylelint.configFile": ".config/stylelint.config.js"
}
```

---

### Jest

**Source:** Root `jest.config.js`
**Target:** `.config/jest.config.js`

**package.json script:**
```json
{
  "scripts": {
    "test": "jest --config .config/jest.config.js",
    "test:watch": "jest --config .config/jest.config.js --watch"
  }
}
```

**jest.config.js adjustment:**
```javascript
// .config/jest.config.js
module.exports = {
  rootDir: '..', // Point back to project root
  testMatch: ['<rootDir>/tests/**/*.test.js'],
  // ... rest of config
};
```

---

### Babel

**Source:** Root `babel.config.js` or `.babelrc`
**Target:** `.config/babel.config.js`

**package.json script:**
```json
{
  "scripts": {
    "build": "babel src --out-dir dist --config-file ./.config/babel.config.js"
  }
}
```

**Notes:**
- Use `--config-file` flag (not `--config`)
- Path must include `./` prefix

---

### Docker

**Source:** Root `Dockerfile`
**Target:** `.config/Dockerfile`

**Build command:**
```bash
docker build -f .config/Dockerfile -t myapp .
```

**docker-compose.yml:**
```yaml
services:
  app:
    build:
      context: .
      dockerfile: .config/Dockerfile
```

**Warning - .dockerignore:**
- `.dockerignore` MUST remain in root (or build context root)
- Docker CLI cannot specify alternate `.dockerignore` location
- This is a known limitation of Docker's design

---

### Environment Variables (.env)

**Source:** Root `.env`
**Target:** `.config/.env`

**Node.js application:**
```javascript
// At application entry point
require('dotenv').config({
  path: require('path').resolve(__dirname, '.config/.env')
});
```

**Framework caveats:**
- **Next.js:** Requires `.env` in root (framework limitation)
- **Create React App:** Requires `.env` in root
- **Vite:** Supports `envDir` option in config

---

## Files That MUST Stay in Root

Some files cannot be moved due to tool limitations:

| File | Reason |
|------|--------|
| `tsconfig.json` | Defines compilation context; moving changes relative paths |
| `.editorconfig` | No plugin supports custom path specification |
| `LICENSE` | GitHub license detection requires root placement |
| `README.md` | Discoverable entry point convention |
| `.gitignore` | Git expects it in repo/working directory root |
| `.gitattributes` | Must be in root for global repo settings |
| `package.json` | Node.js project manifest |
| `.nvmrc` | nvm scans working directory only |
| `.dockerignore` | Docker build context limitation |

## Complete .config/ Example

After migration, your `.config/` directory should look like:

```
.config/
├── eslint.config.js
├── .prettierrc.json
├── stylelint.config.js
├── jest.config.js
├── babel.config.js
├── Dockerfile
├── .env.example      # Template for environment variables
└── commitlint.config.js
```

## Pre-commit Integration

If using pre-commit hooks with Husky or similar:

```json
// package.json
{
  "lint-staged": {
    "*.js": "eslint --config .config/eslint.config.js --fix",
    "*.css": "stylelint --config .config/stylelint.config.js --fix",
    "*": "prettier --config .config/.prettierrc.json --write"
  }
}
```

## CI/CD Pipeline Example

GitHub Actions workflow respecting `.config/` structure:

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint  # Uses --config flag in script
      - run: npm run format:check
```

## Troubleshooting

### ESLint not finding config
- Verify `--config` path is correct relative to where command runs
- Check VS Code `eslint.options.overrideConfigFile` setting

### Prettier not formatting
- Ensure `prettier.configPath` is set in VS Code
- Verify config file extension matches format (`.json`, `.js`, etc.)

### Jest rootDir issues
- When config is in subdirectory, set `rootDir: '..'`
- Use `<rootDir>` prefix in paths within config

### Docker build context
- Remember `-f` specifies Dockerfile, not build context
- Build context (final `.`) is still project root
