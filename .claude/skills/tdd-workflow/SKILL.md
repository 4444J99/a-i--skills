---
name: tdd-workflow
description: Test-driven development workflow with comprehensive coverage requirements including unit, integration, and E2E tests
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  adapted-by: ai-skills
  category: development-workflow
---

# Test-Driven Development Workflow

Enforces test-driven development principles with comprehensive test coverage across all layers.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components
- Implementing business logic

## Core Principles

### 1. Tests BEFORE Code
**Always** write tests first, then implement code to make tests pass. No exceptions.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + E2E)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified
- Happy path and sad path

### 3. Test Pyramid

```
        ┌────────┐
        │   E2E  │  (10-20%)
        ├────────┤
        │  INTEG │  (20-30%)
        ├────────┤
        │  UNIT  │  (50-70%)
        └────────┘
```

## TDD Workflow: Red-Green-Refactor

### Step 1: RED - Write Failing Test

Start with the user story:

```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for products by category,
so that I can find relevant items quickly.
```

Write the test:

```typescript
describe('ProductSearch', () => {
  it('returns products filtered by category', async () => {
    const products = await searchProducts({ category: 'electronics' });
    
    expect(products).toHaveLength(5);
    expect(products.every(p => p.category === 'electronics')).toBe(true);
  });
});
```

### Step 2: Run Tests (They Should Fail)

```bash
npm test
# ✗ ProductSearch > returns products filtered by category
#   TypeError: searchProducts is not a function
```

**This is good!** Red phase confirms test is working.

### Step 3: GREEN - Implement Minimal Code

Write just enough code to pass:

```typescript
export async function searchProducts(filters: SearchFilters) {
  const { category } = filters;
  return db.products.findMany({
    where: { category }
  });
}
```

### Step 4: Run Tests (They Should Pass)

```bash
npm test
# ✓ ProductSearch > returns products filtered by category (42ms)
```

### Step 5: REFACTOR - Improve Code

Now refactor while keeping tests green:

```typescript
export async function searchProducts(filters: SearchFilters) {
  const query = buildSearchQuery(filters);
  const results = await executeSearch(query);
  return transformResults(results);
}
```

Run tests again to ensure they still pass.

## Test Types

### Unit Tests

**Purpose**: Test individual functions in isolation

```typescript
describe('calculateDiscount', () => {
  it('applies 10% discount for basic tier', () => {
    const price = calculateDiscount(100, 'basic');
    expect(price).toBe(90);
  });

  it('applies 20% discount for premium tier', () => {
    const price = calculateDiscount(100, 'premium');
    expect(price).toBe(80);
  });

  it('throws error for invalid tier', () => {
    expect(() => calculateDiscount(100, 'invalid')).toThrow();
  });
});
```

### Integration Tests

**Purpose**: Test multiple components working together

```typescript
describe('User Registration API', () => {
  it('creates user and sends welcome email', async () => {
    const response = await request(app)
      .post('/api/register')
      .send({ email: 'test@example.com', password: 'secret' });  // allow-secret

    expect(response.status).toBe(201);
    expect(response.body.user.email).toBe('test@example.com');
    
    // Verify email was sent
    const sentEmails = await testEmailService.getSentEmails();
    expect(sentEmails).toHaveLength(1);
    expect(sentEmails[0].to).toBe('test@example.com');
  });
});
```

### E2E Tests (Playwright/Cypress)

**Purpose**: Test complete user flows through the UI

```typescript
test('user can complete checkout process', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('[name="cardNumber"]', '4242424242424242');
  await page.click('[data-testid="complete-order"]');

  await expect(page.locator('.success-message')).toBeVisible();
  await expect(page).toHaveURL(/\/order-confirmation/);
});
```

## Coverage Verification

After implementation, check coverage:

```bash
npm test -- --coverage

# Output:
# File          | % Stmts | % Branch | % Funcs | % Lines
# --------------|---------|----------|---------|--------
# All files     |   84.2  |   78.5   |   91.3  |   85.1
```

**Requirements:**
- Statements: > 80%
- Branches: > 75%
- Functions: > 85%
- Lines: > 80%

## Edge Cases Checklist

Always test:

- [ ] Empty input
- [ ] Null/undefined values
- [ ] Large datasets
- [ ] Concurrent operations
- [ ] Network failures
- [ ] Database errors
- [ ] Invalid data types
- [ ] Boundary values (0, -1, MAX_INT)
- [ ] Unauthorized access
- [ ] Rate limiting

## Mocking Strategy

### When to Mock

- External APIs
- Database calls (in unit tests)
- Time-dependent functions
- File system operations
- Third-party services

### Example Mocks

```typescript
// Mock external service
vi.mock('./emailService', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true })
}));

// Mock database
vi.mock('./db', () => ({
  users: {
    findUnique: vi.fn().mockResolvedValue({ id: 1, name: 'Test' })
  }
}));

// Mock Date.now()
vi.spyOn(Date, 'now').mockReturnValue(1234567890000);
```

## Test Organization

```
src/
  features/
    products/
      product.service.ts
      product.service.test.ts      # Unit tests
      product.integration.test.ts  # Integration tests
      product.e2e.test.ts          # E2E tests
```

## Debugging Failed Tests

```bash
# Run single test file
npm test -- product.service.test.ts

# Run single test
npm test -- -t "calculates discount correctly"

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage --no-cache
```

## Integration Points

Complements:
- **verification-loop**: For pre-commit verification
- **testing-patterns**: For test design patterns
- **deployment-cicd**: For CI test execution
- **security-implementation-guide**: For security testing

## Workflow Summary

1. **RED**: Write failing test
2. **GREEN**: Implement minimal code
3. **REFACTOR**: Improve while keeping tests green
4. **VERIFY**: Check coverage meets requirements
5. **COMMIT**: Only commit if all tests pass

Never skip steps. Never commit untested code.
