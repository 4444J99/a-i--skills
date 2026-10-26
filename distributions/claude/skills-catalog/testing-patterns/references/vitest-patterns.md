# Vitest Patterns

Configuration, techniques, and recipes for Vitest.

## Configuration

### Basic Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,           // No need to import describe, it, expect
    environment: 'jsdom',    // For DOM testing (or 'node' for backend)
    setupFiles: ['./test/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.test.*', 'src/**/*.d.ts'],
      thresholds: {
        lines: 80,
        branches: 75,
        functions: 80,
      },
    },
  },
});
```

### Environment Per File

```typescript
// Use a different environment for a specific test file
// @vitest-environment node

import { describe, it, expect } from 'vitest';

describe('server-only utility', () => {
  it('accesses Node.js APIs', () => {
    expect(process.versions.node).toBeDefined();
  });
});
```

## Mocking

### Module Mocks

```typescript
// Mock entire module
vi.mock('./database', () => ({
  db: {
    user: {
      findMany: vi.fn().mockResolvedValue([{ id: '1', name: 'Alice' }]),
      create: vi.fn().mockResolvedValue({ id: '2', name: 'Bob' }),
    },
  },
}));

// Mock with factory that accesses original
vi.mock('./utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./utils')>();
  return {
    ...actual,
    generateId: vi.fn(() => 'mock-id-123'),
  };
});
```

### Spy on Functions

```typescript
import * as mathUtils from './math';

const spy = vi.spyOn(mathUtils, 'calculateTax');
spy.mockReturnValue(10);

calculateOrder(100);
expect(spy).toHaveBeenCalledWith(100, 0.1);

spy.mockRestore(); // Restore original implementation
```

### Mock Timers

```typescript
describe('debounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('calls function after delay', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced();
    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledOnce();
  });
});
```

### Mock Environment Variables

```typescript
describe('config', () => {
  it('reads from environment', () => {
    vi.stubEnv('API_URL', 'https://test.api.com');

    expect(getConfig().apiUrl).toBe('https://test.api.com');

    vi.unstubAllEnvs();
  });
});
```

## Snapshot Testing

```typescript
it('renders user profile correctly', () => {
  const { container } = render(<UserProfile user={mockUser} />);
  expect(container).toMatchSnapshot();
});

// Inline snapshot (stored in the test file)
it('formats date correctly', () => {
  expect(formatDate('2024-01-15')).toMatchInlineSnapshot(`"January 15, 2024"`);
});
```

Update snapshots with `vitest --update` or press `u` in watch mode.

## Parameterized Tests

```typescript
describe('isValidEmail', () => {
  it.each([
    ['user@example.com', true],
    ['user@sub.domain.com', true],
    ['invalid', false],
    ['@no-local.com', false],
    ['no-domain@', false],
    ['', false],
  ])('isValidEmail("%s") should return %s', (email, expected) => {
    expect(isValidEmail(email)).toBe(expected);
  });
});

// With object notation
it.each([
  { input: 0, expected: 'zero' },
  { input: 1, expected: 'one' },
  { input: -1, expected: 'negative' },
])('classify($input) returns "$expected"', ({ input, expected }) => {
  expect(classify(input)).toBe(expected);
});
```

## Testing Async Code

```typescript
// Resolved value
it('fetches user data', async () => {
  const user = await fetchUser('usr_1');
  expect(user.name).toBe('Alice');
});

// Rejected value
it('throws on invalid id', async () => {
  await expect(fetchUser('')).rejects.toThrow('ID is required');
});

// Callbacks (wrap in Promise)
it('emits event', () => {
  return new Promise<void>((resolve) => {
    emitter.on('done', (result) => {
      expect(result).toBe('complete');
      resolve();
    });
    emitter.start();
  });
});
```

## Custom Matchers

```typescript
// test/setup.ts
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () => `expected ${received} to be within [${floor}, ${ceiling}]`,
    };
  },
});

// Usage
expect(randomPort()).toBeWithinRange(1024, 65535);
```

## Workspace Configuration (Monorepo)

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  {
    test: {
      name: 'client',
      root: './packages/client',
      environment: 'jsdom',
    },
  },
  {
    test: {
      name: 'server',
      root: './packages/server',
      environment: 'node',
    },
  },
]);
```

## CLI Commands

| Command | Purpose |
|---------|---------|
| `vitest` | Watch mode |
| `vitest run` | Single run (CI) |
| `vitest run --coverage` | With coverage report |
| `vitest run --reporter=junit` | JUnit output for CI |
| `vitest related src/utils.ts` | Run tests related to file |
| `vitest bench` | Run benchmarks |

## Performance Tips

- Use `vi.mock()` at the top level (hoisted automatically)
- Prefer `vi.fn()` over full module mocks when possible
- Use `--pool=forks` for CPU-intensive tests (isolates better)
- Run `vitest --reporter=verbose` to find slow tests
- Use `test.concurrent` for independent async tests
