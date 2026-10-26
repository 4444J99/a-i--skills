# Observability Configuration

Setup patterns for monitoring, logging, and alerting in production applications.

## The Three Pillars

| Pillar | What | Tools |
|--------|------|-------|
| **Metrics** | Numeric measurements over time | Prometheus, Datadog, CloudWatch |
| **Logs** | Discrete events with context | Pino, Winston, Datadog Logs |
| **Traces** | Request flow across services | OpenTelemetry, Jaeger, Zipkin |

## Application Metrics

### Prometheus with Express/Node

```typescript
import { collectDefaultMetrics, Counter, Histogram, Registry } from 'prom-client';

const registry = new Registry();
collectDefaultMetrics({ register: registry });

// Custom metrics
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  registers: [registry],
});

const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [registry],
});

// Middleware
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    const labels = { method: req.method, route: req.route?.path || req.path, status: res.statusCode };
    end(labels);
    httpRequestTotal.inc(labels);
  });
  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', registry.contentType);
  res.send(await registry.metrics());
});
```

### Key Metrics to Track

| Category | Metric | Why |
|----------|--------|-----|
| Latency | p50, p95, p99 response time | Detect degradation |
| Traffic | Requests per second | Capacity planning |
| Errors | Error rate (5xx / total) | Reliability |
| Saturation | CPU, memory, connections | Resource limits |

These are the **four golden signals** from the Google SRE handbook.

## Structured Logging

### Pino Setup

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
  redact: ['req.headers.authorization', 'req.headers.cookie'],
});

// Request-scoped logging
app.use((req, res, next) => {
  req.log = logger.child({
    requestId: req.headers['x-request-id'] || crypto.randomUUID(),
    method: req.method,
    url: req.url,
  });
  next();
});

// Usage
req.log.info({ userId: user.id }, 'User authenticated');
req.log.error({ err, orderId }, 'Payment processing failed');
```

### Log Levels

| Level | When to Use |
|-------|-------------|
| `fatal` | App is about to crash |
| `error` | Operation failed, needs attention |
| `warn` | Unexpected but handled |
| `info` | Normal operations (request served, job completed) |
| `debug` | Detailed diagnostic info |
| `trace` | Very granular, usually disabled |

Production: set level to `info` or `warn`.

### What to Log

```typescript
// Good: structured, actionable, contextual
logger.info({ userId: 'usr_123', action: 'login', ip: req.ip }, 'User logged in');
logger.error({ err, orderId: 'ord_456', amount: 99.99 }, 'Payment failed');

// Bad: unstructured, missing context
logger.info('User logged in');
logger.error('Something went wrong');
```

## Error Tracking with Sentry

```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,  // 10% of transactions
  integrations: [
    Sentry.httpIntegration(),
    Sentry.expressIntegration(),
    Sentry.prismaIntegration(),
  ],
});

// Express error handler (must be last)
app.use(Sentry.expressErrorHandler());

// Manual capture
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: { feature: 'payments' },
    extra: { orderId: 'ord_456' },
  });
}
```

## Health Check Endpoint

```typescript
app.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    externalApi: await checkExternalApi(),
  };

  const healthy = Object.values(checks).every(c => c.status === 'up');

  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks,
  });
});

async function checkDatabase(): Promise<HealthCheck> {
  try {
    await db.$queryRaw`SELECT 1`;
    return { status: 'up', latency: '2ms' };
  } catch {
    return { status: 'down', error: 'Connection failed' };
  }
}
```

## Alerting Rules

### Common Alert Conditions

| Alert | Condition | Severity |
|-------|-----------|----------|
| High error rate | 5xx rate > 1% for 5 minutes | Critical |
| High latency | p95 > 2s for 5 minutes | Warning |
| Service down | Health check failing for 2 minutes | Critical |
| Disk usage | > 80% capacity | Warning |
| Memory usage | > 90% for 10 minutes | Critical |
| Certificate expiry | < 14 days remaining | Warning |

### PagerDuty / Slack Integration

```yaml
# In your monitoring tool (e.g., Grafana)
alerting:
  - name: high-error-rate
    condition: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
    for: 5m
    notify:
      - slack: '#alerts-critical'
      - pagerduty: production-oncall
```

## Uptime Monitoring

External uptime checks complement internal health endpoints.

| Tool | Type | Use For |
|------|------|---------|
| UptimeRobot | HTTP ping | Basic uptime |
| Better Uptime | Multi-location | Global availability |
| Checkly | Synthetic monitoring | E2E user flow checks |

Configure checks from multiple regions and set up status pages for public-facing services.

## Dashboard Essentials

A production dashboard should show at a glance:

1. **Request rate** -- current vs. baseline
2. **Error rate** -- percentage and absolute count
3. **Latency distribution** -- p50, p95, p99
4. **Active users / connections** -- load indicator
5. **Infrastructure** -- CPU, memory, disk per host
6. **Deployment markers** -- when deploys happened

Keep dashboards focused: one for service health, one for business metrics.
