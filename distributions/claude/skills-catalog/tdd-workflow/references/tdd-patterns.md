# TDD Patterns Reference

Test-Driven Development patterns and practices.

## The TDD Cycle

```
┌──────────────────────────────────────────────┐
│                                              │
│    ┌─────┐         ┌─────┐         ┌─────┐  │
│    │ RED │ ──────→ │GREEN│ ──────→ │REFAC│  │
│    └─────┘         └─────┘         └─────┘  │
│       ↑                               │      │
│       └───────────────────────────────┘      │
│                                              │
└──────────────────────────────────────────────┘

RED:    Write a failing test
GREEN:  Write minimal code to pass
REFACTOR: Improve code, tests still pass
```

## Test Structure: AAA Pattern

```typescript
describe('Calculator', () => {
  it('should add two numbers', () => {
    // Arrange
    const calculator = new Calculator();

    // Act
    const result = calculator.add(2, 3);

    // Assert
    expect(result).toBe(5);
  });
});
```

## Test Naming Conventions

### Pattern 1: Should + Behavior

```typescript
it('should return null when user not found')
it('should throw error when email is invalid')
it('should emit event when state changes')
```

### Pattern 2: Given/When/Then

```typescript
describe('given a valid user', () => {
  describe('when updating email', () => {
    it('then saves the new email')
    it('then sends confirmation email')
  });
});
```

### Pattern 3: Unit Under Test + Scenario + Expected

```typescript
describe('UserService.createUser', () => {
  it('with valid data creates user')
  it('with duplicate email throws ConflictError')
  it('with missing name throws ValidationError')
});
```

## Test Doubles

### Stub: Returns canned data

```typescript
const userRepository = {
  findById: jest.fn().mockResolvedValue({ id: 1, name: 'John' })
};
```

### Mock: Verifies interactions

```typescript
const emailService = {
  send: jest.fn()
};

// Later
expect(emailService.send).toHaveBeenCalledWith({
  to: 'user@example.com',
  subject: 'Welcome'
});
```

### Spy: Real object, recorded calls

```typescript
const spy = jest.spyOn(console, 'log');
// ... do something
expect(spy).toHaveBeenCalled();
spy.mockRestore();
```

### Fake: Working implementation

```typescript
class FakeUserRepository implements UserRepository {
  private users: User[] = [];

  async save(user: User) {
    this.users.push(user);
  }

  async findById(id: string) {
    return this.users.find(u => u.id === id);
  }
}
```

## Test Patterns

### Test Fixture

```typescript
describe('OrderService', () => {
  let orderService: OrderService;
  let userRepository: FakeUserRepository;

  // Shared setup
  beforeEach(() => {
    userRepository = new FakeUserRepository();
    orderService = new OrderService(userRepository);
  });

  // Shared teardown
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('creates order', () => {
    // Test uses shared setup
  });
});
```

### Test Data Builder

```typescript
class UserBuilder {
  private user: Partial<User> = {
    id: '1',
    name: 'Default Name',
    email: 'default@example.com',
    status: 'active'
  };

  withId(id: string) {
    this.user.id = id;
    return this;
  }

  withName(name: string) {
    this.user.name = name;
    return this;
  }

  inactive() {
    this.user.status = 'inactive';
    return this;
  }

  build(): User {
    return this.user as User;
  }
}

// Usage
const user = new UserBuilder().withName('John').inactive().build();
```

### Parameterized Tests

```typescript
describe('isValidEmail', () => {
  const validCases = [
    'user@example.com',
    'user.name@example.com',
    'user+tag@example.com'
  ];

  const invalidCases = [
    'not-an-email',
    '@example.com',
    'user@'
  ];

  validCases.forEach(email => {
    it(`should accept ${email}`, () => {
      expect(isValidEmail(email)).toBe(true);
    });
  });

  invalidCases.forEach(email => {
    it(`should reject ${email}`, () => {
      expect(isValidEmail(email)).toBe(false);
    });
  });
});
```

## Red-Green-Refactor in Practice

### Step 1: Write Failing Test

```typescript
// Start with the simplest case
describe('FizzBuzz', () => {
  it('returns "1" for 1', () => {
    expect(fizzBuzz(1)).toBe('1');
  });
});
```

### Step 2: Make it Pass (Minimal)

```typescript
function fizzBuzz(n: number): string {
  return '1'; // Simplest thing that works
}
```

### Step 3: Add Next Test

```typescript
it('returns "2" for 2', () => {
  expect(fizzBuzz(2)).toBe('2');
});
```

### Step 4: Generalize

```typescript
function fizzBuzz(n: number): string {
  return String(n);
}
```

### Step 5: Continue Pattern

```typescript
it('returns "Fizz" for 3', () => {
  expect(fizzBuzz(3)).toBe('Fizz');
});

// Implementation evolves...
```

## Testing Pyramid

```
          /\
         /  \       E2E Tests (Few)
        /----\
       /      \     Integration Tests (Some)
      /--------\
     /          \   Unit Tests (Many)
    /------------\
```

| Level | Scope | Speed | Count |
|-------|-------|-------|-------|
| Unit | Single function/class | Fast | Many |
| Integration | Multiple components | Medium | Some |
| E2E | Full system | Slow | Few |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing implementation | Fragile tests | Test behavior |
| One assertion per test (extreme) | Too many tests | Group related assertions |
| Testing private methods | Coupling to internals | Test via public interface |
| Flaky tests | Unreliable CI | Fix or quarantine |
| Slow tests | Long feedback loop | Mock external dependencies |
| Test after code | Miss edge cases | Write tests first |

## TDD Benefits Checklist

- [ ] Tests document behavior
- [ ] Design emerges from usage
- [ ] Refactoring is safe
- [ ] Bugs are caught early
- [ ] Code is naturally testable
- [ ] Minimal code written
