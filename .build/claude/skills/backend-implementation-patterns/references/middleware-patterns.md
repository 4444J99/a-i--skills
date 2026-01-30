# Backend Middleware Patterns

Common middleware patterns for Express/Node.js backends.

## Middleware Order

Recommended middleware stack order:

```typescript
// 1. Security headers
app.use(helmet());

// 2. CORS
app.use(cors(corsOptions));

// 3. Request parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// 4. Request logging
app.use(requestLogger);

// 5. Rate limiting
app.use(rateLimiter);

// 6. Authentication
app.use('/api', authMiddleware);

// 7. Routes
app.use('/api', routes);

// 8. Error handling (must be last)
app.use(errorHandler);
```

## Request Logging

```typescript
function requestLogger(req, res, next) {
  const start = Date.now();
  const requestId = crypto.randomUUID();

  req.requestId = requestId;
  res.setHeader('X-Request-Id', requestId);

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      requestId,
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration,
      userAgent: req.get('user-agent'),
      ip: req.ip
    }));
  });

  next();
}
```

## Authentication Middleware

### JWT Verification

```typescript
async function authMiddleware(req, res, next) {
  // Skip auth for public routes
  const publicRoutes = ['/api/auth/login', '/api/auth/register'];
  if (publicRoutes.includes(req.path)) {
    return next();
  }

  const authHeader = req.headers.authorization; // allow-secret
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'Missing authorization header' }
    });
  }

  const token = authHeader.split(' ')[1]; // allow-secret

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET); // allow-secret
    req.user = payload;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        error: { code: 'TOKEN_EXPIRED', message: 'Token has expired' }
      });
    }
    return res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Invalid token' }
    });
  }
}
```

### Role-Based Access

```typescript
function requireRole(...roles: string[]) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        error: { code: 'UNAUTHORIZED', message: 'Authentication required' }
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' }
      });
    }

    next();
  };
}

// Usage
app.delete('/api/users/:id', requireRole('admin'), deleteUser);
```

## Validation Middleware

```typescript
import { z } from 'zod';

function validate(schema: z.ZodSchema) {
  return (req, res, next) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params
    });

    if (!result.success) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request data',
          details: result.error.errors.map(err => ({
            field: err.path.join('.'),
            message: err.message
          }))
        }
      });
    }

    req.validated = result.data;
    next();
  };
}

// Usage
const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    name: z.string().min(2)
  })
});

app.post('/api/users', validate(createUserSchema), createUser);
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

// Standard rate limit
const standardLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      success: false,
      error: {
        code: 'RATE_LIMITED',
        message: 'Too many requests',
        retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
      }
    });
  }
});

// Strict limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 attempts
  skipSuccessfulRequests: true
});

app.use('/api/', standardLimiter);
app.use('/api/auth/login', authLimiter);
```

## Error Handling Middleware

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message);
  }
}

function errorHandler(err, req, res, next) {
  // Log error
  console.error({
    requestId: req.requestId,
    error: err.message,
    stack: err.stack,
    path: req.path
  });

  // Known errors
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        details: err.details
      }
    });
  }

  // Validation errors (Zod, Joi, etc.)
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: err.message
      }
    });
  }

  // Database errors
  if (err.code === '23505') { // Postgres unique violation
    return res.status(409).json({
      success: false,
      error: {
        code: 'DUPLICATE_ENTRY',
        message: 'Resource already exists'
      }
    });
  }

  // Unknown errors
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : err.message
    }
  });
}
```

## CORS Configuration

```typescript
const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      'https://app.example.com',
      process.env.NODE_ENV === 'development' && 'http://localhost:3000'
    ].filter(Boolean);

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
};
```

## Request Context

```typescript
import { AsyncLocalStorage } from 'async_hooks';

const requestContext = new AsyncLocalStorage<{
  requestId: string;
  userId?: string;
}>();

function contextMiddleware(req, res, next) {
  const context = {
    requestId: req.requestId,
    userId: req.user?.id
  };

  requestContext.run(context, () => next());
}

// Use anywhere in code
function getContext() {
  return requestContext.getStore();
}
```
