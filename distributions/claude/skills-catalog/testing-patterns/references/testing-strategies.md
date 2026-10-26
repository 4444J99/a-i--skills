# Testing Strategies Reference

Comprehensive testing patterns for different scenarios.

## Test Types Overview

| Type | Purpose | Speed | Scope |
|------|---------|-------|-------|
| Unit | Test isolated logic | Very fast | Function/class |
| Integration | Test component interaction | Medium | Module/service |
| E2E | Test full user flows | Slow | Entire system |
| Smoke | Verify critical paths | Fast | Key features |
| Regression | Catch regressions | Varies | Changed areas |

## Unit Testing Patterns

### Pure Function Testing

```typescript
// Function with no side effects
function calculateDiscount(price: number, percentage: number): number {
  return price * (1 - percentage / 100);
}

describe('calculateDiscount', () => {
  it('applies 10% discount correctly', () => {
    expect(calculateDiscount(100, 10)).toBe(90);
  });

  it('handles 0% discount', () => {
    expect(calculateDiscount(100, 0)).toBe(100);
  });

  it('handles 100% discount', () => {
    expect(calculateDiscount(100, 100)).toBe(0);
  });
});
```

### Class Testing

```typescript
describe('ShoppingCart', () => {
  let cart: ShoppingCart;

  beforeEach(() => {
    cart = new ShoppingCart();
  });

  describe('addItem', () => {
    it('adds item to cart', () => {
      cart.addItem({ id: '1', price: 10 });
      expect(cart.itemCount).toBe(1);
    });

    it('increments quantity for duplicate items', () => {
      cart.addItem({ id: '1', price: 10 });
      cart.addItem({ id: '1', price: 10 });
      expect(cart.itemCount).toBe(1);
      expect(cart.getItem('1')?.quantity).toBe(2);
    });
  });

  describe('total', () => {
    it('calculates total correctly', () => {
      cart.addItem({ id: '1', price: 10 });
      cart.addItem({ id: '2', price: 20 });
      expect(cart.total).toBe(30);
    });
  });
});
```

## Integration Testing Patterns

### Database Integration

```typescript
describe('UserRepository', () => {
  let db: Database;
  let repo: UserRepository;

  beforeAll(async () => {
    db = await Database.connect(TEST_DB_URL);
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.query('DELETE FROM users');
    repo = new UserRepository(db);
  });

  it('creates and retrieves user', async () => {
    const user = await repo.create({ name: 'John', email: 'john@test.com' });

    const found = await repo.findById(user.id);

    expect(found).toMatchObject({
      name: 'John',
      email: 'john@test.com'
    });
  });
});
```

### API Integration

```typescript
describe('POST /api/users', () => {
  it('creates user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@test.com' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      name: 'John',
      email: 'john@test.com'
    });
  });

  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'invalid' })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## E2E Testing Patterns

### Page Object Pattern

```typescript
// pages/LoginPage.ts
class LoginPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) { // allow-secret
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async getErrorMessage() {
    return this.page.textContent('[data-testid="error"]');
  }
}

// tests/login.spec.ts
describe('Login', () => {
  let loginPage: LoginPage;

  beforeEach(async () => {
    loginPage = new LoginPage(page);
    await loginPage.navigate();
  });

  it('logs in with valid credentials', async () => {
    await loginPage.login('user@test.com', 'password123');
    await expect(page).toHaveURL('/dashboard');
  });

  it('shows error for invalid credentials', async () => {
    await loginPage.login('user@test.com', 'wrong');
    expect(await loginPage.getErrorMessage()).toContain('Invalid');
  });
});
```

## Mocking Strategies

### Dependency Injection

```typescript
// Production
class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDTO) {
    const user = await this.userRepo.create(data);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}

// Test
describe('UserService', () => {
  it('sends welcome email on user creation', async () => {
    const mockRepo = { create: jest.fn().mockResolvedValue({ id: '1', email: 'test@test.com' }) };
    const mockEmail = { sendWelcome: jest.fn() };

    const service = new UserService(mockRepo, mockEmail);
    await service.createUser({ name: 'Test', email: 'test@test.com' });

    expect(mockEmail.sendWelcome).toHaveBeenCalledWith('test@test.com');
  });
});
```

### Module Mocking

```typescript
// Mock entire module
jest.mock('./emailService', () => ({
  sendEmail: jest.fn()
}));

import { sendEmail } from './emailService';

describe('notification', () => {
  it('sends email notification', async () => {
    await sendNotification('user@test.com', 'Hello');
    expect(sendEmail).toHaveBeenCalled();
  });
});
```

## Test Data Management

### Factory Functions

```typescript
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    createdAt: new Date(),
    ...overrides
  };
}

// Usage
const activeUser = createUser({ status: 'active' });
const adminUser = createUser({ role: 'admin' });
```

### Seeding

```typescript
async function seedTestData(db: Database) {
  const users = Array.from({ length: 10 }, () => createUser());
  await db.users.insertMany(users);
  return { users };
}

beforeEach(async () => {
  await db.truncateAll();
  testData = await seedTestData(db);
});
```

## Async Testing

### Waiting for Conditions

```typescript
// Wait for element
await page.waitForSelector('[data-testid="result"]');

// Wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.click('[data-testid="submit"]')
]);

// Wait for network idle
await page.waitForLoadState('networkidle');

// Custom wait
await expect(async () => {
  const count = await page.locator('.item').count();
  expect(count).toBeGreaterThan(0);
}).toPass({ timeout: 5000 });
```

### Testing Timeouts

```typescript
describe('retryOperation', () => {
  it('retries on failure', async () => {
    const operation = jest.fn()
      .mockRejectedValueOnce(new Error('Fail'))
      .mockRejectedValueOnce(new Error('Fail'))
      .mockResolvedValueOnce('Success');

    const result = await retryOperation(operation, { maxRetries: 3 });

    expect(result).toBe('Success');
    expect(operation).toHaveBeenCalledTimes(3);
  }, 10000); // Increase timeout for retry tests
});
```

## Coverage Goals

| Metric | Recommended | Critical Code |
|--------|-------------|---------------|
| Line | 70-80% | 90%+ |
| Branch | 70-80% | 90%+ |
| Function | 80%+ | 95%+ |

Focus on meaningful coverage, not just hitting numbers.
