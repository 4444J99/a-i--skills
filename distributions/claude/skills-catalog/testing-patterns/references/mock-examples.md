# Mocking Recipes

Practical mocking patterns for common testing scenarios using Vitest.

## API Calls with fetch

### Basic fetch mock

```typescript
const mockFetch = vi.fn();
global.fetch = mockFetch;

beforeEach(() => {
  mockFetch.mockReset();
});

it('fetches users', async () => {
  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [{ id: '1', name: 'Alice' }],
  });

  const users = await getUsers();

  expect(mockFetch).toHaveBeenCalledWith('/api/users', expect.any(Object));
  expect(users).toHaveLength(1);
});

it('handles fetch failure', async () => {
  mockFetch.mockResolvedValueOnce({
    ok: false,
    status: 500,
    json: async () => ({ error: 'Server error' }),
  });

  await expect(getUsers()).rejects.toThrow('Failed to fetch users');
});
```

### MSW (Mock Service Worker) for Realistic Mocks

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ]);
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '3', ...body }, { status: 201 });
  }),

  http.delete('/api/users/:id', ({ params }) => {
    return new HttpResponse(null, { status: 204 });
  }),
];

// mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// test/setup.ts
import { server } from '../mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Override handler in a specific test

```typescript
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';

it('shows error when API fails', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ error: 'Database error' }, { status: 500 });
    }),
  );

  render(<UserList />);
  await expect(screen.findByText(/something went wrong/i)).resolves.toBeInTheDocument();
});
```

## Database and ORM Mocks

### Prisma mock

```typescript
// test/mocks/prisma.ts
import { vi } from 'vitest';

export const prismaMock = {
  user: {
    findMany: vi.fn(),
    findUnique: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
  post: {
    findMany: vi.fn(),
    create: vi.fn(),
  },
  $transaction: vi.fn((cb) => cb(prismaMock)),
};

vi.mock('@/lib/db', () => ({
  db: prismaMock,
}));
```

```typescript
import { prismaMock } from '../mocks/prisma';

it('creates user and returns it', async () => {
  const expected = { id: '1', name: 'Alice', email: 'alice@test.com' };
  prismaMock.user.create.mockResolvedValue(expected);

  const result = await createUser({ name: 'Alice', email: 'alice@test.com' });

  expect(prismaMock.user.create).toHaveBeenCalledWith({
    data: { name: 'Alice', email: 'alice@test.com' },
  });
  expect(result).toEqual(expected);
});
```

## React Hooks

### Mock a custom hook

```typescript
vi.mock('@/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

import { useAuth } from '@/hooks/useAuth';

it('shows dashboard for authenticated user', () => {
  vi.mocked(useAuth).mockReturnValue({
    user: { id: '1', name: 'Alice' },
    isLoading: false,
    isAuthenticated: true,
  });

  render(<Dashboard />);
  expect(screen.getByText('Welcome, Alice')).toBeInTheDocument();
});

it('redirects when not authenticated', () => {
  vi.mocked(useAuth).mockReturnValue({
    user: null,
    isLoading: false,
    isAuthenticated: false,
  });

  render(<Dashboard />);
  expect(screen.getByText(/please log in/i)).toBeInTheDocument();
});
```

## Timers and Dates

### Fixed date

```typescript
it('displays relative time', () => {
  vi.setSystemTime(new Date('2024-06-15T12:00:00Z'));

  const result = formatRelativeTime(new Date('2024-06-15T11:00:00Z'));
  expect(result).toBe('1 hour ago');

  vi.useRealTimers();
});
```

### Debounce/throttle testing

```typescript
it('debounces search input', async () => {
  vi.useFakeTimers();
  const onSearch = vi.fn();
  render(<SearchInput onSearch={onSearch} debounceMs={300} />);

  await userEvent.type(screen.getByRole('textbox'), 'hello');

  expect(onSearch).not.toHaveBeenCalled();

  vi.advanceTimersByTime(300);
  expect(onSearch).toHaveBeenCalledWith('hello');

  vi.useRealTimers();
});
```

## External Services

### Email service mock

```typescript
vi.mock('@/lib/email', () => ({
  sendEmail: vi.fn().mockResolvedValue({ messageId: 'mock-id' }),
}));

import { sendEmail } from '@/lib/email';

it('sends welcome email on signup', async () => {
  await signupUser({ name: 'Alice', email: 'alice@test.com' });

  expect(sendEmail).toHaveBeenCalledWith({
    to: 'alice@test.com',
    subject: 'Welcome!',
    template: 'welcome',
    data: { name: 'Alice' },
  });
});
```

### File system mock

```typescript
vi.mock('fs/promises', () => ({
  readFile: vi.fn(),
  writeFile: vi.fn(),
  mkdir: vi.fn(),
}));

import { readFile, writeFile } from 'fs/promises';

it('reads config file', async () => {
  vi.mocked(readFile).mockResolvedValue(
    JSON.stringify({ theme: 'dark' }),
  );

  const config = await loadConfig('/path/to/config.json');
  expect(config.theme).toBe('dark');
});
```

## Randomness and UUIDs

```typescript
vi.mock('crypto', async (importOriginal) => {
  const actual = await importOriginal<typeof import('crypto')>();
  return {
    ...actual,
    randomUUID: vi.fn(() => '00000000-0000-0000-0000-000000000001'),
  };
});

it('generates predictable IDs', () => {
  const item = createItem({ name: 'Test' });
  expect(item.id).toBe('00000000-0000-0000-0000-000000000001');
});
```

## When to Mock vs. When to Integrate

| Scenario | Mock | Integrate |
|----------|------|-----------|
| External API (Stripe, GitHub) | Yes (MSW) | In dedicated integration tests |
| Database in unit tests | Yes | No |
| Database in integration tests | No | Yes (test DB) |
| File system | Yes in unit tests | Yes in integration |
| Time/Date | Yes | No |
| Sibling module | Rarely | Usually import real module |
| Third-party React component | Rarely | Render the real thing |

**Rule of thumb**: Mock at the boundary. The more you mock, the less your tests resemble real usage.
