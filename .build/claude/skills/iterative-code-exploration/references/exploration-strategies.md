# Code Exploration Strategies

Systematic approaches to understanding unfamiliar codebases.

## Initial Assessment

### Quick Codebase Survey

1. **Read the README** - Project purpose, setup, architecture
2. **Check package.json/requirements.txt** - Dependencies reveal patterns
3. **Look at directory structure** - Understand organization
4. **Find the entry point** - main.ts, index.js, App.tsx
5. **Identify key abstractions** - Core classes, types, interfaces

### Questions to Answer

- What problem does this solve?
- What's the tech stack?
- What patterns are used (MVC, Clean Architecture, etc.)?
- How is state managed?
- How are tests organized?

## Exploration Techniques

### Top-Down: Entry Point Tracing

Start from entry point, follow execution path.

```
main.ts
  └─> App.tsx
        └─> Router
              └─> Pages
                    └─> Components
                          └─> Services
                                └─> API calls
```

### Bottom-Up: Dependency Analysis

Start from low-level utilities, understand building blocks.

```
utils/
  └─> hooks/
        └─> components/
              └─> pages/
                    └─> App
```

### Middle-Out: Feature Focus

Pick one feature, trace it completely.

```
Feature: User Login

UI: LoginForm.tsx
  ↓ calls
API: authService.login()
  ↓ sends to
Backend: POST /api/auth/login
  ↓ validates with
Database: users table
```

## Search Strategies

### Finding Functionality

| Looking For | Search Pattern |
|-------------|----------------|
| Where X is used | Search: `functionName(` or `<ComponentName` |
| Where X is defined | Search: `function functionName` or `const X =` |
| Where X is imported | Search: `import.*X` or `require.*X` |
| API endpoints | Search: `app.get`, `router.post`, `/api/` |
| Environment vars | Search: `process.env`, `import.meta.env` |
| Error handling | Search: `catch`, `try`, `throw` |

### Grep Patterns

```bash
# Find function definitions
grep -r "function handleSubmit" src/

# Find component usage
grep -r "<UserProfile" src/

# Find type definitions
grep -r "interface User" src/

# Find API calls
grep -r "fetch\|axios" src/

# Find TODO/FIXME
grep -r "TODO\|FIXME\|HACK" src/
```

## Understanding Code Flow

### Call Graph

For a function, map:
- What calls this function?
- What does this function call?
- What data flows in/out?

```
callers → [function] → callees
           ↓     ↑
         input  output
```

### Data Flow

Trace data through the system:

```
User Input → Validation → Transform → Store → Query → Display
```

### Event Flow

For event-driven code:

```
Event Source → Event Bus → Handlers → Side Effects
```

## Annotation Strategies

### Code Comments (Temporary)

```typescript
// EXPLORATION: This function is called from LoginPage
// EXPLORATION: Sends POST to /api/auth
// EXPLORATION: Returns user object with token
async function login(credentials) {
  // ...
}
```

### Notes File

```markdown
# Codebase Notes

## Key Files
- `src/App.tsx` - Main entry, sets up providers
- `src/api/client.ts` - Axios instance with interceptors
- `src/store/index.ts` - Redux store setup

## Patterns Observed
- Container/Presenter pattern for pages
- Services layer for API calls
- Custom hooks for business logic

## Questions
- [ ] How is auth state persisted?
- [ ] What happens on token expiry?
- [ ] Where are feature flags configured?

## Discoveries
- Auth token stored in localStorage (security concern?)
- Retry logic in API client (3 attempts)
- WebSocket used for real-time updates
```

## Debugging Exploration

### Adding Trace Points

```typescript
// Temporary: trace execution
console.log('[TRACE] Entering handleSubmit', { formData });

// Temporary: trace state changes
useEffect(() => {
  console.log('[TRACE] user state changed', user);
}, [user]);
```

### Breakpoint Strategy

Set breakpoints at:
1. Entry points (event handlers, API endpoints)
2. Data transformations
3. Conditional branches
4. Error handling

## Incremental Understanding

### The "Three Pass" Method

**Pass 1: Skim**
- Read file names and folder structure
- Scan imports and exports
- Note public APIs

**Pass 2: Connect**
- Trace one feature end-to-end
- Map component relationships
- Understand data flow

**Pass 3: Detail**
- Read implementation details
- Understand edge cases
- Note patterns and anti-patterns

### Time-Boxed Exploration

| Time | Goal |
|------|------|
| 15 min | High-level architecture |
| 30 min | One feature traced |
| 1 hour | Core patterns understood |
| 2 hours | Ready to make changes |

## Documentation You Create

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│               Frontend                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Pages  │→ │Components│→ │  Hooks  │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│        ↓           ↓            ↓       │
│  ┌─────────────────────────────────────┐│
│  │           State (Redux)              ││
│  └─────────────────────────────────────┘│
│        ↓                                 │
│  ┌─────────────────────────────────────┐│
│  │         API Client (axios)           ││
│  └─────────────────────────────────────┘│
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│                Backend                   │
│  Routes → Controllers → Services → DB   │
└─────────────────────────────────────────┘
```

### Glossary

Document domain-specific terms:
- **Widget** - A configurable dashboard component
- **Tenant** - A customer organization
- **Plan** - Subscription tier
