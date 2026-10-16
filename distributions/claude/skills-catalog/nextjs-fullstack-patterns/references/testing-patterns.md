# Testing Next.js Applications

Patterns for unit, integration, and E2E testing of Next.js App Router applications.

## Testing Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Unit/Integration | Vitest + Testing Library | Component and utility tests |
| E2E | Playwright | Full browser user flows |
| API | Vitest + supertest or direct calls | Route handler testing |
| Visual | Playwright screenshots | Visual regression |

## Vitest Setup for Next.js

```bash
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./test/setup.ts'],
    include: ['**/*.test.{ts,tsx}'],
    alias: {
      '@': resolve(__dirname, './'),
    },
  },
});
```

```typescript
// test/setup.ts
import '@testing-library/jest-dom/vitest';
```

## Testing Server Components

Server Components cannot be directly rendered in jsdom. Test their logic or render them in E2E tests.

### Extract and test the logic

```typescript
// lib/posts.ts
export async function getPublishedPosts() {
  return db.post.findMany({ where: { status: 'published' }, orderBy: { createdAt: 'desc' } });
}

// lib/posts.test.ts
describe('getPublishedPosts', () => {
  it('returns only published posts in desc order', async () => {
    await db.post.createMany({
      data: [
        { title: 'Draft', status: 'draft', createdAt: new Date('2024-01-01') },
        { title: 'Old', status: 'published', createdAt: new Date('2024-01-01') },
        { title: 'New', status: 'published', createdAt: new Date('2024-02-01') },
      ],
    });

    const posts = await getPublishedPosts();
    expect(posts).toHaveLength(2);
    expect(posts[0].title).toBe('New');
  });
});
```

## Testing Client Components

```tsx
// components/SearchBar.tsx
'use client';

import { useState } from 'react';

export function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSearch(query); }}>
      <input
        type="search"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">Search</button>
    </form>
  );
}

// components/SearchBar.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SearchBar } from './SearchBar';

describe('SearchBar', () => {
  it('calls onSearch with input value on submit', async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();
    render(<SearchBar onSearch={onSearch} />);

    await user.type(screen.getByPlaceholderText('Search...'), 'nextjs');
    await user.click(screen.getByRole('button', { name: /search/i }));

    expect(onSearch).toHaveBeenCalledWith('nextjs');
  });
});
```

## Testing Server Actions

```typescript
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  if (!title || title.length < 3) {
    return { error: 'Title must be at least 3 characters' };
  }
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
  return { success: true };
}

// app/actions.test.ts
vi.mock('next/cache', () => ({
  revalidatePath: vi.fn(),
}));

describe('createPost', () => {
  it('returns error for short title', async () => {
    const formData = new FormData();
    formData.set('title', 'ab');

    const result = await createPost(formData);
    expect(result.error).toBe('Title must be at least 3 characters');
  });

  it('creates post and revalidates', async () => {
    const formData = new FormData();
    formData.set('title', 'My New Post');

    const result = await createPost(formData);
    expect(result.success).toBe(true);
    expect(revalidatePath).toHaveBeenCalledWith('/posts');
  });
});
```

## Testing API Route Handlers

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const posts = await db.post.findMany();
  return NextResponse.json(posts);
}

// app/api/posts/route.test.ts
import { GET } from './route';
import { NextRequest } from 'next/server';

describe('GET /api/posts', () => {
  it('returns posts as JSON', async () => {
    await db.post.create({ data: { title: 'Test Post' } });

    const request = new NextRequest('http://localhost/api/posts');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toHaveLength(1);
    expect(data[0].title).toBe('Test Post');
  });
});
```

## E2E with Playwright

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
});
```

### User Flow Test

```typescript
// e2e/create-post.spec.ts
import { test, expect } from '@playwright/test';

test('user can create and view a post', async ({ page }) => {
  await page.goto('/posts/new');

  await page.fill('[name="title"]', 'E2E Test Post');
  await page.fill('[name="content"]', 'Content from Playwright');
  await page.click('button[type="submit"]');

  // Redirected to post page
  await expect(page).toHaveURL(/\/posts\/.+/);
  await expect(page.locator('h1')).toContainText('E2E Test Post');
});
```

### Auth Setup with Storage State

```typescript
// e2e/auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'testpassword');
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');

  await page.context().storageState({ path: 'e2e/.auth/user.json' });
});

// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/ },
  {
    name: 'authenticated',
    use: { storageState: 'e2e/.auth/user.json' },
    dependencies: ['setup'],
  },
]
```

## Mocking Next.js Internals

```typescript
// Common mocks for testing
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), back: vi.fn() }),
  usePathname: () => '/test',
  useSearchParams: () => new URLSearchParams(),
  redirect: vi.fn(),
  notFound: vi.fn(),
}));

vi.mock('next/headers', () => ({
  cookies: () => ({ get: vi.fn(), set: vi.fn() }),
  headers: () => new Headers(),
}));
```

## CI Pipeline

```yaml
# .github/workflows/test.yml
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npx vitest run --coverage

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```
