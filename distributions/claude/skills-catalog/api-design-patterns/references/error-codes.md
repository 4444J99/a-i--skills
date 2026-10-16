# Standard API Error Codes

Consistent error codes for API responses.

## HTTP Status Code Mapping

### 4xx Client Errors

| Code | HTTP Status | Description | When to Use |
|------|-------------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data | Schema validation failed |
| `INVALID_FORMAT` | 400 | Malformed request | JSON parsing failed, wrong content-type |
| `MISSING_FIELD` | 400 | Required field missing | Required parameter not provided |
| `INVALID_VALUE` | 400 | Invalid field value | Enum mismatch, out of range |
| `UNAUTHORIZED` | 401 | Authentication required | No token or invalid token |
| `TOKEN_EXPIRED` | 401 | Token has expired | JWT expired |
| `INVALID_CREDENTIALS` | 401 | Wrong credentials | Bad username/password |
| `FORBIDDEN` | 403 | Insufficient permissions | Valid auth, no access |
| `NOT_FOUND` | 404 | Resource not found | ID doesn't exist |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not supported | Wrong HTTP verb |
| `CONFLICT` | 409 | State conflict | Duplicate, version conflict |
| `DUPLICATE_ENTRY` | 409 | Already exists | Unique constraint violation |
| `GONE` | 410 | Resource deleted | Permanently removed |
| `PAYLOAD_TOO_LARGE` | 413 | Request too large | File upload too big |
| `UNPROCESSABLE_ENTITY` | 422 | Semantic error | Valid syntax, invalid logic |
| `RATE_LIMITED` | 429 | Too many requests | Rate limit exceeded |

### 5xx Server Errors

| Code | HTTP Status | Description | When to Use |
|------|-------------|-------------|-------------|
| `INTERNAL_ERROR` | 500 | Unexpected server error | Unhandled exception |
| `DATABASE_ERROR` | 500 | Database operation failed | Query/connection error |
| `EXTERNAL_SERVICE_ERROR` | 502 | Third-party failure | External API error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily down | Maintenance, overload |
| `TIMEOUT` | 504 | Request timed out | Operation took too long |

## Error Response Structure

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      },
      {
        "field": "age",
        "code": "INVALID_VALUE",
        "message": "Must be at least 18"
      }
    ],
    "requestId": "req_abc123xyz",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Domain-Specific Error Codes

### Authentication

| Code | Description |
|------|-------------|
| `AUTH_REQUIRED` | Must be logged in |
| `SESSION_EXPIRED` | Session no longer valid |
| `MFA_REQUIRED` | Two-factor required |
| `MFA_INVALID` | Wrong MFA code |
| `ACCOUNT_LOCKED` | Too many failed attempts |
| `ACCOUNT_DISABLED` | Account deactivated |

### User Management

| Code | Description |
|------|-------------|
| `USER_NOT_FOUND` | User doesn't exist |
| `EMAIL_TAKEN` | Email already registered |
| `USERNAME_TAKEN` | Username already in use |
| `WEAK_PASSWORD` | Password doesn't meet requirements |
| `EMAIL_NOT_VERIFIED` | Email verification required |

### Payments

| Code | Description |
|------|-------------|
| `PAYMENT_FAILED` | Payment processing error |
| `INSUFFICIENT_FUNDS` | Not enough balance |
| `CARD_DECLINED` | Card was declined |
| `CARD_EXPIRED` | Card is expired |
| `INVALID_CARD` | Invalid card number |
| `SUBSCRIPTION_REQUIRED` | Feature requires subscription |
| `SUBSCRIPTION_EXPIRED` | Subscription no longer active |

### File Operations

| Code | Description |
|------|-------------|
| `FILE_TOO_LARGE` | Exceeds size limit |
| `INVALID_FILE_TYPE` | File type not allowed |
| `UPLOAD_FAILED` | File upload error |
| `FILE_NOT_FOUND` | File doesn't exist |
| `STORAGE_FULL` | Storage quota exceeded |

## Error Code Best Practices

### Naming Convention

```
CATEGORY_SPECIFIC_ISSUE

Examples:
- AUTH_TOKEN_EXPIRED
- PAYMENT_CARD_DECLINED
- USER_EMAIL_TAKEN
- FILE_TOO_LARGE
```

### Include in Response

1. **code**: Machine-readable error code
2. **message**: Human-readable description
3. **details**: Array of specific issues (for validation)
4. **requestId**: For debugging/support
5. **timestamp**: When error occurred

### What NOT to Expose

- Stack traces
- Internal server paths
- Database schema details
- Specific library versions
- Raw SQL errors

## Client Handling Example

```typescript
async function handleAPIError(error: APIError) {
  switch (error.code) {
    case 'UNAUTHORIZED':
    case 'TOKEN_EXPIRED':
      await refreshToken();
      return retry();

    case 'RATE_LIMITED':
      const retryAfter = error.retryAfter || 60;
      await delay(retryAfter * 1000);
      return retry();

    case 'VALIDATION_ERROR':
      showFieldErrors(error.details);
      break;

    case 'NOT_FOUND':
      showNotFoundPage();
      break;

    default:
      showGenericError();
  }
}
```
