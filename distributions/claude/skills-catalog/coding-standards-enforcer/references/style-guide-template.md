# Coding Standards Template

Customizable template for team coding standards.

## General Principles

### Code Clarity

- Write code for humans first, computers second
- Prefer explicit over implicit
- Avoid clever tricks that sacrifice readability
- Use meaningful names that reveal intent

### Consistency

- Follow existing patterns in the codebase
- When in doubt, match surrounding code
- Document exceptions to standards

---

## Naming Conventions

### Variables

| Type | Convention | Example |
|------|------------|---------|
| Local variables | camelCase | `userName`, `itemCount` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| Boolean | is/has/can/should prefix | `isValid`, `hasItems` |
| Collections | Plural noun | `users`, `items` |

### Functions

| Type | Convention | Example |
|------|------------|---------|
| Regular function | camelCase, verb phrase | `getUserById`, `calculateTotal` |
| Event handler | handle + Event | `handleClick`, `handleSubmit` |
| Boolean return | is/has/can/should | `isValidEmail`, `canAccess` |
| Factory | create + Noun | `createUser`, `createConnection` |

### Classes

| Type | Convention | Example |
|------|------------|---------|
| Class | PascalCase | `UserService`, `PaymentProcessor` |
| Interface | PascalCase (I-prefix optional) | `User`, `IUserRepository` |
| Enum | PascalCase | `Status`, `UserRole` |
| Enum values | SCREAMING_SNAKE | `PENDING`, `ACTIVE` |

### Files

| Type | Convention | Example |
|------|------------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Utility | kebab-case | `string-utils.ts` |
| Test | *.test.ts or *.spec.ts | `user.test.ts` |
| Types | *.types.ts | `user.types.ts` |

---

## Code Structure

### File Organization

```
// 1. Imports (grouped)
import { external } from 'external-lib';
import { internal } from '@/internal';
import { local } from './local';

// 2. Types/Interfaces
interface Props { ... }

// 3. Constants
const DEFAULT_VALUE = 10;

// 4. Main export
export function Component() { ... }

// 5. Helper functions (private)
function helperFunction() { ... }
```

### Function Length

- **Target**: < 20 lines
- **Maximum**: 50 lines (consider refactoring)
- Extract helper functions for clarity

### Nesting Depth

- **Target**: ≤ 3 levels
- Use early returns (guard clauses)
- Extract to separate functions

---

## Error Handling

### Error Messages

```typescript
// Good - specific and actionable
throw new Error(`User not found with ID: ${id}`);

// Bad - vague
throw new Error('Error occurred');
```

### Try/Catch Scope

```typescript
// Good - narrow scope
try {
  const user = await fetchUser(id);
} catch (error) {
  handleFetchError(error);
}

// Bad - too broad
try {
  const user = await fetchUser(id);
  const posts = await fetchPosts(user.id);
  const comments = await fetchComments(posts);
  // ...many more operations
} catch (error) {
  // What failed?
}
```

---

## Comments

### When to Comment

| Comment | Don't Comment |
|---------|---------------|
| Why code exists | What code does (code should be clear) |
| Business rules | Obvious operations |
| Workarounds and reasons | Redundant information |
| Public API documentation | Implementation details |

### Comment Style

```typescript
// Single line for brief explanations

/**
 * Multi-line for documentation.
 * Explains purpose, parameters, return values.
 */

// TODO: Include ticket reference (TODO: PROJ-123)
// FIXME: Include ticket reference
// HACK: Explain why and ticket for proper fix
```

---

## Testing

### Test Naming

```typescript
// Pattern: should_expectedBehavior_when_condition
it('should return null when user not found', () => {});
it('should throw error when email is invalid', () => {});

// Or: description of behavior
it('returns null for non-existent user', () => {});
```

### Test Structure

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('creates user with valid data', () => {
      // Arrange
      const data = { name: 'John', email: 'john@test.com' };

      // Act
      const result = userService.createUser(data);

      // Assert
      expect(result.name).toBe('John');
    });
  });
});
```

---

## TypeScript Specific

### Type Annotations

```typescript
// Annotate function parameters and return types
function greet(name: string): string {
  return `Hello, ${name}`;
}

// Infer local variables when obvious
const count = 0; // number is inferred

// Annotate when not obvious
const config: AppConfig = getConfig();
```

### Prefer

| Prefer | Over |
|--------|------|
| `interface` | `type` (for objects) |
| `unknown` | `any` |
| Type guards | Type assertions |
| Strict mode | Loose mode |

---

## Git Commits

### Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When |
|------|------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting |
| refactor | Code restructuring |
| test | Adding tests |
| chore | Build, tooling |

### Example

```
feat(auth): add password reset flow

Implement password reset via email link.
Includes token generation and expiry validation.

Closes #123
```

---

## Linting & Formatting

### Required Tools

- ESLint with recommended config
- Prettier for formatting
- TypeScript strict mode
- Pre-commit hooks (husky + lint-staged)

### Auto-fix on Save

Configure IDE to:
- Format on save (Prettier)
- Fix lint errors on save (ESLint)
- Organize imports on save
