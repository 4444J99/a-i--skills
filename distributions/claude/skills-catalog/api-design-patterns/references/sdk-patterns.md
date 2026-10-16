# Client SDK Design Patterns

Patterns for building and structuring client SDKs that wrap REST or GraphQL APIs.

## SDK Architecture

### Layered Structure

```
Application Code
      │
  SDK Client          ← Public API (type-safe methods)
      │
  Request Builder     ← Constructs HTTP requests
      │
  HTTP Transport      ← Handles retries, auth, serialization
      │
  Network (fetch/axios)
```

### Client Initialization

```typescript
import { MyServiceClient } from 'my-service-sdk';

const client = new MyServiceClient({
  apiKey: process.env.API_KEY,  // allow-secret
  baseUrl: 'https://api.example.com/v1',  // Optional override
  timeout: 30_000,                         // ms
  retries: 3,
});
```

## Resource-Based Design

Organize methods by resource, mirroring the API structure.

```typescript
// Resource-based access
const user = await client.users.get('usr_123');
const posts = await client.users.posts.list('usr_123', { page: 1 });

// CRUD operations follow a consistent pattern
await client.users.list({ status: 'active', page: 2 });
await client.users.create({ name: 'Alice', email: 'alice@example.com' });
await client.users.update('usr_123', { name: 'Alice B.' });
await client.users.delete('usr_123');
```

### Implementation

```typescript
class UsersResource {
  constructor(private http: HttpClient) {}

  async list(params?: ListUsersParams): Promise<PaginatedResponse<User>> {
    return this.http.get('/users', { params });
  }

  async get(id: string): Promise<User> {
    return this.http.get(`/users/${id}`);
  }

  async create(data: CreateUserInput): Promise<User> {
    return this.http.post('/users', data);
  }

  async update(id: string, data: UpdateUserInput): Promise<User> {
    return this.http.patch(`/users/${id}`, data);
  }

  async delete(id: string): Promise<void> {
    return this.http.delete(`/users/${id}`);
  }
}
```

## Error Handling

### Typed SDK Errors

```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public requestId?: string,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

class ValidationError extends ApiError {
  constructor(
    message: string,
    public details: FieldError[],
    requestId?: string,
  ) {
    super(400, 'VALIDATION_ERROR', message, requestId);
  }
}

class NotFoundError extends ApiError {
  constructor(resource: string, id: string) {
    super(404, 'NOT_FOUND', `${resource} '${id}' not found`);
  }
}
```

### Client-Side Error Handling

```typescript
try {
  const user = await client.users.get('usr_missing');
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log('User does not exist');
  } else if (error instanceof ApiError) {
    console.log(`API error: ${error.code} — ${error.message}`);
  } else {
    throw error; // Network or unexpected error
  }
}
```

## Pagination

### Iterator Pattern

```typescript
// Automatic pagination with async iterators
for await (const user of client.users.listAll({ status: 'active' })) {
  console.log(user.name);
}

// Implementation
async *listAll(params?: ListUsersParams): AsyncGenerator<User> {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const response = await this.list({ ...params, page });
    for (const item of response.data) {
      yield item;
    }
    hasMore = response.meta.page < Math.ceil(response.meta.total / response.meta.perPage);
    page++;
  }
}
```

### Page Object Pattern

```typescript
const page = await client.users.list({ perPage: 20 });

console.log(page.data);         // User[]
console.log(page.meta.total);   // 150
console.log(page.hasMore());    // true

const nextPage = await page.next();
```

## Retry and Rate Limiting

```typescript
class HttpClient {
  async request<T>(config: RequestConfig): Promise<T> {
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await fetch(config.url, config.options);

        if (response.status === 429) {
          const retryAfter = parseInt(response.headers.get('Retry-After') || '1');
          await this.sleep(retryAfter * 1000);
          continue;
        }

        if (response.status >= 500 && attempt < this.maxRetries) {
          await this.sleep(Math.pow(2, attempt) * 1000); // Exponential backoff
          continue;
        }

        return this.handleResponse(response);
      } catch (error) {
        if (attempt === this.maxRetries) throw error;
      }
    }
  }
}
```

## Configuration Patterns

### Environment-Aware Defaults

```typescript
interface ClientConfig {
  apiKey: string;       // allow-secret
  baseUrl?: string;     // Default from environment
  timeout?: number;     // Default: 30000
  retries?: number;     // Default: 2
  logger?: Logger;      // Default: no-op
}

// Auto-detect from environment
const client = new MyServiceClient({
  apiKey: process.env.MY_SERVICE_API_KEY!,  // allow-secret
  // baseUrl defaults to process.env.MY_SERVICE_BASE_URL or production URL
});
```

### Middleware / Interceptors

```typescript
const client = new MyServiceClient({
  apiKey: 'key',  // allow-secret
  middleware: [
    loggingMiddleware(),
    metricsMiddleware(),
    customHeaderMiddleware({ 'X-Custom': 'value' }),
  ],
});
```

## TypeScript Best Practices

| Practice | Why |
|----------|-----|
| Export all request/response types | Consumers can use them for their own types |
| Use branded types for IDs (`UserId`, `PostId`) | Prevents passing wrong ID type |
| Make optional fields explicit (`field?: Type`) | Clear API contract |
| Return `Promise<T>` not `Promise<any>` | Full type safety |
| Use discriminated unions for errors | Enables exhaustive error handling |
| Generate types from OpenAPI spec | Single source of truth |

### Type Generation

```bash
# Generate TypeScript types from OpenAPI
npx openapi-typescript openapi.yaml -o src/types/api.ts

# Generate full SDK client
npx @hey-api/openapi-ts -i openapi.yaml -o src/generated
```

## Testing the SDK

```typescript
describe('UsersResource', () => {
  let client: MyServiceClient;

  beforeEach(() => {
    client = new MyServiceClient({
      apiKey: 'test-key',  // allow-secret
      baseUrl: 'http://localhost:4010', // Prism mock server
    });
  });

  it('lists users with pagination', async () => {
    const result = await client.users.list({ page: 1, perPage: 10 });
    expect(result.data).toHaveLength(10);
    expect(result.meta.page).toBe(1);
  });

  it('throws NotFoundError for missing user', async () => {
    await expect(client.users.get('nonexistent'))
      .rejects.toThrow(NotFoundError);
  });
});
```

Use [Prism](https://stoplight.io/open-source/prism) to mock an API server from your OpenAPI spec for SDK testing.
