// sentry.server.config.ts
// Server-side Sentry configuration

import * as Sentry from '@sentry/nextjs';

// Environment resolution
function resolveEnvironment(): string | undefined {
  if (process.env.SENTRY_ENVIRONMENT) {
    return process.env.SENTRY_ENVIRONMENT;
  }
  const vercelEnv = process.env.VERCEL_ENV;
  if (vercelEnv === 'production') return 'production';
  if (vercelEnv === 'preview') return 'preview';
  if (vercelEnv === 'development') return 'development';
  return process.env.NODE_ENV;
}

// PII Redaction
const EMAIL_PATTERN = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const REDACTED = '[REDACTED]';
const SENSITIVE_HEADERS = new Set([
  'authorization',
  'cookie',
  'set-cookie',
  'x-api-key',
  'x-auth-token',
]);

function sanitizeString(str: string): string {
  return str.replace(EMAIL_PATTERN, REDACTED);
}

function sanitizeHeaders(
  headers?: Record<string, string>
): Record<string, string> | undefined {
  if (!headers) return undefined;
  const sanitized: Record<string, string> = {};
  for (const [key, value] of Object.entries(headers)) {
    if (SENSITIVE_HEADERS.has(key.toLowerCase())) {
      sanitized[key] = REDACTED;
    } else {
      sanitized[key] = sanitizeString(value);
    }
  }
  return sanitized;
}

function sanitizeEvent(event: Sentry.Event): Sentry.Event {
  // Redact user email
  if (event.user?.email) {
    event.user.email = REDACTED;
  }
  // Remove IP address
  if (event.user?.ip_address) {
    delete event.user.ip_address;
  }
  // Sanitize request headers
  if (event.request?.headers) {
    event.request.headers = sanitizeHeaders(event.request.headers);
  }
  // Sanitize message
  if (event.message) {
    event.message = sanitizeString(event.message);
  }
  return event;
}

// Sample rate parsing
function parseSampleRate(envVar: string | undefined, defaultValue: number): number {
  if (!envVar) return defaultValue;
  const parsed = parseFloat(envVar);
  return isNaN(parsed) ? defaultValue : Math.max(0, Math.min(1, parsed));
}

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: resolveEnvironment(),

  // Security: Disable default PII collection
  sendDefaultPii: false,

  // Performance monitoring
  tracesSampleRate: parseSampleRate(
    process.env.SENTRY_TRACES_SAMPLE_RATE,
    0.1 // 10% default
  ),

  // PII sanitization
  beforeSend: (event, hint) => {
    return sanitizeEvent(event);
  },

  // Breadcrumb sanitization
  beforeBreadcrumb: (breadcrumb) => {
    if (breadcrumb.message) {
      breadcrumb.message = sanitizeString(breadcrumb.message);
    }
    return breadcrumb;
  },
});
