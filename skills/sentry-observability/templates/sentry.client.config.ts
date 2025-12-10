// sentry.client.config.ts
// Client-side Sentry configuration with PII redaction

import * as Sentry from '@sentry/nextjs';

// Environment resolution
function resolveEnvironment(): string | undefined {
  if (process.env.SENTRY_ENVIRONMENT) {
    return process.env.SENTRY_ENVIRONMENT;
  }
  const vercelEnv = process.env.NEXT_PUBLIC_VERCEL_ENV;
  if (vercelEnv === 'production') return 'production';
  if (vercelEnv === 'preview') return 'preview';
  if (vercelEnv === 'development') return 'development';
  return process.env.NODE_ENV;
}

// PII Redaction
const EMAIL_PATTERN = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const REDACTED = '[REDACTED]';

function sanitizeString(str: string): string {
  return str.replace(EMAIL_PATTERN, REDACTED);
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
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: resolveEnvironment(),

  // Security: Disable default PII collection
  sendDefaultPii: false,

  // Performance monitoring
  tracesSampleRate: parseSampleRate(
    process.env.NEXT_PUBLIC_SENTRY_TRACES_SAMPLE_RATE,
    0.1 // 10% default
  ),

  // Session Replay
  replaysSessionSampleRate: parseSampleRate(
    process.env.NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE,
    0 // Disabled by default (cost-aware)
  ),
  replaysOnErrorSampleRate: parseSampleRate(
    process.env.NEXT_PUBLIC_SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE,
    1.0 // 100% on errors
  ),

  // PII sanitization
  beforeSend: (event, hint) => {
    return sanitizeEvent(event);
  },

  // Filter noisy errors
  ignoreErrors: [
    // Browser extension errors
    /chrome-extension/,
    /moz-extension/,
    // Network errors that are usually user-side
    'Network request failed',
    'Failed to fetch',
    'Load failed',
    // Aborted requests
    'AbortError',
  ],

  // Integrations
  integrations: [
    Sentry.replayIntegration({
      // Mask all text and block all media by default (privacy)
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
});
