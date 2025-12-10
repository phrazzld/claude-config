# PII Redaction

Security-critical patterns for removing Personally Identifiable Information from Sentry events.

## Why This Matters

- Privacy regulations (GDPR, CCPA) require PII protection
- Sentry events are stored for 90 days
- Team members with Sentry access can see all event data
- Compliance violations can result in significant fines

## Core Implementation

```typescript
// lib/sentry.ts

const EMAIL_REDACTION_PATTERN = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const EMAIL_REDACTED = '[EMAIL_REDACTED]';
const SENSITIVE_HEADERS = new Set([
  'authorization',
  'cookie',
  'set-cookie',
  'x-api-key',
  'x-auth-token',
  'x-session-id',
]);

export function sanitizeEvent(event: Event, _hint?: EventHint): Event {
  // 1. Redact user email
  if (event.user?.email) {
    event.user.email = EMAIL_REDACTED;
  }

  // 2. Remove IP address
  if (event.user?.ip_address) {
    delete event.user.ip_address;
  }

  // 3. Sanitize request headers
  if (event.request?.headers) {
    event.request.headers = sanitizeHeaders(event.request.headers);
  }

  // 4. Sanitize request data (body)
  if (event.request?.data) {
    event.request.data = sanitizeObject(event.request.data);
  }

  // 5. Sanitize contexts
  if (event.contexts) {
    event.contexts = sanitizeObject(event.contexts);
  }

  // 6. Sanitize extra
  if (event.extra) {
    event.extra = sanitizeObject(event.extra);
  }

  // 7. Sanitize tags
  if (event.tags) {
    for (const [key, value] of Object.entries(event.tags)) {
      if (typeof value === 'string') {
        event.tags[key] = redactEmails(value);
      }
    }
  }

  // 8. Sanitize message
  if (event.message) {
    event.message = redactEmails(event.message);
  }

  return event;
}

function sanitizeHeaders(headers: Record<string, string>): Record<string, string> {
  const sanitized: Record<string, string> = {};
  for (const [key, value] of Object.entries(headers)) {
    if (SENSITIVE_HEADERS.has(key.toLowerCase())) {
      sanitized[key] = '[REDACTED]';
    } else {
      sanitized[key] = redactEmails(value);
    }
  }
  return sanitized;
}

function redactEmails(str: string): string {
  return str.replace(EMAIL_REDACTION_PATTERN, EMAIL_REDACTED);
}

function sanitizeObject(obj: unknown): unknown {
  if (typeof obj === 'string') {
    return redactEmails(obj);
  }
  if (Array.isArray(obj)) {
    return obj.map(sanitizeObject);
  }
  if (obj && typeof obj === 'object') {
    const sanitized: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj)) {
      // Skip sensitive keys entirely
      if (isSensitiveKey(key)) {
        sanitized[key] = '[REDACTED]';
      } else {
        sanitized[key] = sanitizeObject(value);
      }
    }
    return sanitized;
  }
  return obj;
}

function isSensitiveKey(key: string): boolean {
  const lowerKey = key.toLowerCase();
  return (
    lowerKey.includes('password') ||
    lowerKey.includes('secret') ||
    lowerKey.includes('token') ||
    lowerKey.includes('apikey') ||
    lowerKey.includes('api_key') ||
    lowerKey.includes('credit_card') ||
    lowerKey.includes('ssn') ||
    lowerKey.includes('social_security')
  );
}
```

## Breadcrumb Sanitization

```typescript
export function sanitizeBreadcrumb(breadcrumb: Breadcrumb): Breadcrumb {
  if (breadcrumb.message) {
    breadcrumb.message = redactEmails(breadcrumb.message);
  }
  if (breadcrumb.data) {
    breadcrumb.data = sanitizeObject(breadcrumb.data) as Record<string, unknown>;
  }
  return breadcrumb;
}
```

## Sentry Init Configuration

```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN,

  // CRITICAL: Disable default PII collection
  sendDefaultPii: false,

  // Apply sanitization to all events
  beforeSend: (event, hint) => sanitizeEvent(event, hint),

  // Apply sanitization to all breadcrumbs
  beforeBreadcrumb: (breadcrumb) => sanitizeBreadcrumb(breadcrumb),
});
```

## What Gets Redacted

| Data Type | Action |
|-----------|--------|
| User emails | `[EMAIL_REDACTED]` |
| IP addresses | Deleted |
| Authorization headers | `[REDACTED]` |
| Cookies | `[REDACTED]` |
| API keys | `[REDACTED]` |
| Passwords | `[REDACTED]` |
| Tokens | `[REDACTED]` |

## Testing PII Redaction

```typescript
// Test that emails are redacted
const event = {
  user: { email: 'test@example.com' },
  message: 'Error for user test@example.com',
};

const sanitized = sanitizeEvent(event);
expect(sanitized.user.email).toBe('[EMAIL_REDACTED]');
expect(sanitized.message).toBe('Error for user [EMAIL_REDACTED]');
```

## Additional Recommendations

1. **Never log user credentials** in your application code
2. **Use Sentry's data scrubbing** as a backup (Settings > Security > Data Scrubbing)
3. **Review events periodically** to catch any PII leaks
4. **Document your PII handling** for compliance audits
