# Playwright E2E Patterns

Configuration, patterns, and recipes for end-to-end testing with Playwright.

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'mobile', use: { ...devices['iPhone 14'] } },
  ],
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

## Page Object Model

```typescript
// e2e/pages/DashboardPage.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class DashboardPage {
  readonly heading: Locator;
  readonly statsCards: Locator;
  readonly createButton: Locator;

  constructor(private page: Page) {
    this.heading = page.getByRole('heading', { name: /dashboard/i });
    this.statsCards = page.getByTestId('stats-card');
    this.createButton = page.getByRole('button', { name: /create/i });
  }

  async goto() {
    await this.page.goto('/dashboard');
    await expect(this.heading).toBeVisible();
  }

  async getStatValue(label: string): Promise<string> {
    const card = this.page.getByTestId('stats-card').filter({ hasText: label });
    return (await card.getByTestId('stat-value').textContent()) ?? '';
  }

  async clickCreate() {
    await this.createButton.click();
  }
}

// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';
import { DashboardPage } from './pages/DashboardPage';

test('displays stats on dashboard', async ({ page }) => {
  const dashboard = new DashboardPage(page);
  await dashboard.goto();

  const revenue = await dashboard.getStatValue('Revenue');
  expect(revenue).not.toBe('');
});
```

## Authentication Setup

### Global auth setup (runs once)

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate as user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('testpassword');
  await page.getByRole('button', { name: /sign in/i }).click();
  await expect(page).toHaveURL('/dashboard');

  // Save browser state for reuse
  await page.context().storageState({ path: 'e2e/.auth/user.json' });
});
```

```typescript
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'tests',
    dependencies: ['setup'],
    use: { storageState: 'e2e/.auth/user.json' },
  },
]
```

## Locator Strategies

Prefer user-facing locators in this order:

```typescript
// 1. Role (best: accessible and resilient)
page.getByRole('button', { name: /submit/i });
page.getByRole('link', { name: 'Home' });
page.getByRole('heading', { level: 1 });

// 2. Label (for form fields)
page.getByLabel('Email address');

// 3. Placeholder
page.getByPlaceholder('Search...');

// 4. Text content
page.getByText('Welcome back');

// 5. Test ID (last resort)
page.getByTestId('submit-button');
```

## Common Patterns

### Waiting for network requests

```typescript
test('submits form and waits for API', async ({ page }) => {
  await page.goto('/create');

  const responsePromise = page.waitForResponse('**/api/posts');
  await page.getByRole('button', { name: /save/i }).click();
  const response = await responsePromise;

  expect(response.status()).toBe(201);
});
```

### File upload

```typescript
test('uploads a profile photo', async ({ page }) => {
  await page.goto('/settings');

  const fileInput = page.getByLabel('Upload photo');
  await fileInput.setInputFiles('e2e/fixtures/avatar.png');

  await expect(page.getByAltText('Profile photo')).toBeVisible();
});
```

### Dialog handling

```typescript
test('confirms deletion', async ({ page }) => {
  page.on('dialog', async (dialog) => {
    expect(dialog.message()).toContain('Are you sure?');
    await dialog.accept();
  });

  await page.getByRole('button', { name: /delete/i }).click();
  await expect(page.getByText('Item deleted')).toBeVisible();
});
```

### Intercepting and mocking API responses

```typescript
test('displays error state', async ({ page }) => {
  await page.route('**/api/posts', (route) => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Internal server error' }),
    });
  });

  await page.goto('/posts');
  await expect(page.getByText(/something went wrong/i)).toBeVisible();
});
```

## Visual Regression

```typescript
test('homepage matches screenshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.01,
  });
});

// Update screenshots: npx playwright test --update-snapshots
```

Screenshots are stored in `e2e/__screenshots__/` and committed to source control.

## Fixtures

### Custom fixtures

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test';
import { DashboardPage } from './pages/DashboardPage';

type MyFixtures = {
  dashboardPage: DashboardPage;
};

export const test = base.extend<MyFixtures>({
  dashboardPage: async ({ page }, use) => {
    const dashboard = new DashboardPage(page);
    await dashboard.goto();
    await use(dashboard);
  },
});

export { expect } from '@playwright/test';

// e2e/dashboard.spec.ts
import { test, expect } from './fixtures';

test('dashboard loads', async ({ dashboardPage }) => {
  // dashboardPage is already navigated and ready
  await expect(dashboardPage.heading).toBeVisible();
});
```

## Debugging

| Command | Purpose |
|---------|---------|
| `npx playwright test --ui` | Interactive UI mode |
| `npx playwright test --debug` | Step-through debugger |
| `npx playwright show-report` | Open HTML report |
| `npx playwright codegen localhost:3000` | Record actions and generate code |
| `PWDEBUG=1 npx playwright test` | Inspector mode |

### Trace viewer

```bash
# View trace from failed test
npx playwright show-trace test-results/my-test/trace.zip
```

Traces include screenshots at each step, DOM snapshots, network logs, and console output.

## CI Tips

- Use `workers: 1` in CI for stability
- Set `retries: 2` to handle flaky infrastructure
- Upload `playwright-report/` as an artifact on failure
- Run E2E tests after unit tests (fail fast)
- Use a dedicated test database seeded before each run
