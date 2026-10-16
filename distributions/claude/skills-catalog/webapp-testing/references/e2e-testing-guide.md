# E2E Testing Guide

End-to-end testing patterns for web applications.

## Test Framework Comparison

| Framework | Language | Best For |
|-----------|----------|----------|
| Playwright | JS/TS/Python | Modern, cross-browser |
| Cypress | JS/TS | Developer experience |
| Selenium | Many | Legacy, wide support |
| Puppeteer | JS | Chrome-specific |

## Playwright Patterns

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    await page.fill('[data-testid="email"]', 'user@test.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.fill('[data-testid="email"]', 'user@test.com');
    await page.fill('[data-testid="password"]', 'wrong');
    await page.click('[data-testid="submit"]');

    await expect(page.locator('[data-testid="error"]')).toBeVisible();
  });
});
```

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) { // allow-secret
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async getError() {
    return this.page.textContent('[data-testid="error"]');
  }
}

// pages/DashboardPage.ts
export class DashboardPage {
  constructor(private page: Page) {}

  async expectLoaded() {
    await expect(this.page).toHaveURL('/dashboard');
    await expect(this.page.locator('h1')).toBeVisible();
  }

  async getUserName() {
    return this.page.textContent('[data-testid="user-name"]');
  }
}

// tests/auth.spec.ts
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const dashboard = new DashboardPage(page);

  await loginPage.goto();
  await loginPage.login('user@test.com', 'password123');
  await dashboard.expectLoaded();
});
```

### Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';

type TestFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<TestFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup: login
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'user@test.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');
    await page.waitForURL('/dashboard');

    // Provide the page
    await use(page);

    // Teardown: logout
    await page.click('[data-testid="logout"]');
  },
});

// Usage
test('authenticated user can see profile', async ({ authenticatedPage }) => {
  await authenticatedPage.click('[data-testid="profile-link"]');
  await expect(authenticatedPage).toHaveURL('/profile');
});
```

## Cypress Patterns

### Basic Commands

```typescript
describe('Shopping Cart', () => {
  beforeEach(() => {
    cy.visit('/products');
  });

  it('adds product to cart', () => {
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();

    cy.get('[data-testid="cart-count"]').should('contain', '1');
  });

  it('removes product from cart', () => {
    // Add first
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();

    // Remove
    cy.get('[data-testid="cart-icon"]').click();
    cy.get('[data-testid="remove-item"]').click();

    cy.get('[data-testid="cart-count"]').should('contain', '0');
  });
});
```

### Custom Commands

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => { // allow-secret
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="submit"]').click();
  cy.url().should('include', '/dashboard');
});

Cypress.Commands.add('apiLogin', (email: string, password: string) => { // allow-secret
  cy.request('POST', '/api/auth/login', { email, password })
    .its('body')
    .then((body) => {
      window.localStorage.setItem('token', body.token);
    });
});

// Usage
cy.login('user@test.com', 'password123');
cy.apiLogin('user@test.com', 'password123'); // Faster, no UI
```

## Test Selectors

### Best Practices

```html
<!-- Good: data-testid -->
<button data-testid="submit-button">Submit</button>

<!-- Acceptable: role + accessible name -->
<button aria-label="Submit form">Submit</button>

<!-- Avoid: CSS classes (can change) -->
<button class="btn btn-primary">Submit</button>

<!-- Avoid: Element structure (fragile) -->
<div class="form"><button>Submit</button></div>
```

### Selector Priority

1. `data-testid` - Most stable, explicit for testing
2. Role + Name - Accessible and meaningful
3. Label text - For form elements
4. Placeholder - For inputs
5. CSS selectors - Last resort

## Waiting Strategies

### Auto-Wait (Playwright)

```typescript
// Playwright auto-waits for elements
await page.click('button'); // Waits for button to be visible

// Explicit waits when needed
await page.waitForSelector('.loading', { state: 'hidden' });
await page.waitForResponse('/api/data');
await page.waitForLoadState('networkidle');
```

### Cypress Auto-Retry

```typescript
// Cypress automatically retries assertions
cy.get('.result').should('contain', 'Success');

// Explicit waits
cy.wait('@apiCall'); // Wait for intercepted request
cy.get('.loading').should('not.exist');
```

## Network Mocking

### Playwright

```typescript
await page.route('/api/users', (route) => {
  route.fulfill({
    status: 200,
    body: JSON.stringify([{ id: 1, name: 'Test User' }])
  });
});

// Or from file
await page.route('/api/users', route => route.fulfill({
  path: './fixtures/users.json'
}));
```

### Cypress

```typescript
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');

// Or inline
cy.intercept('POST', '/api/login', {
  statusCode: 200,
  body: { token: 'fake-token' } // allow-secret
});

// Wait for intercepted request
cy.wait('@getUsers');
```

## Visual Testing

```typescript
// Playwright screenshot comparison
await expect(page).toHaveScreenshot('homepage.png');

// With threshold
await expect(page).toHaveScreenshot('chart.png', {
  maxDiffPixels: 100
});

// Element screenshot
await expect(page.locator('.card')).toHaveScreenshot();
```

## Test Organization

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── logout.spec.ts
│   ├── products/
│   │   ├── browse.spec.ts
│   │   └── search.spec.ts
│   └── checkout/
│       └── purchase.spec.ts
├── fixtures/
│   ├── users.json
│   └── products.json
└── pages/
    ├── LoginPage.ts
    └── ProductPage.ts
```

## CI Configuration

```yaml
# GitHub Actions
- name: Run E2E Tests
  uses: docker://mcr.microsoft.com/playwright:v1.40.0-jammy
  run: npx playwright test

# With sharding
- name: Run E2E Tests
  run: npx playwright test --shard=${{ matrix.shard }}/${{ matrix.total }}
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
      total: [4]
```
