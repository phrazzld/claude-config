import type { Breadcrumb, Event, EventHint } from "@sentry/nextjs";

// Centralized Sentry options with PII scrubbing shared across runtimes.

const EMAIL_PATTERN =
  /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const EMAIL_REDACTED = "[EMAIL_REDACTED]";
const SENSITIVE_HEADERS = new Set([
  "authorization",
  "cookie",
  "set-cookie",
  "x-api-key",
]);

type SentryTarget = "client" | "server" | "edge";

export type SentryInitOptions = Record<string, unknown> & {
  enabled: boolean;
};

function parseSampleRate(value: string | undefined, fallback: number): number {
  if (!value) return fallback;
  const parsed = Number.parseFloat(value);
  if (Number.isNaN(parsed)) return fallback;
  return Math.min(Math.max(parsed, 0), 1);
}

function sanitizeString(value: string): string {
  return value.replace(EMAIL_PATTERN, EMAIL_REDACTED);
}

function sanitizeHeaders(
  headers: Record<string, unknown> | undefined
): Record<string, unknown> | undefined {
  if (!headers) return headers;
  for (const [key, rawValue] of Object.entries(headers)) {
    if (SENSITIVE_HEADERS.has(key.toLowerCase())) {
      delete headers[key];
      continue;
    }
    if (typeof rawValue === "string") {
      headers[key] = sanitizeString(rawValue);
    } else if (Array.isArray(rawValue)) {
      headers[key] = rawValue.map((item) =>
        typeof item === "string" ? sanitizeString(item) : item
      );
    }
  }
  return headers;
}

function sanitizeValue<T>(value: T, seen: WeakSet<object>): T {
  if (!value) return value;
  if (typeof value === "string") return sanitizeString(value) as T;
  if (Array.isArray(value))
    return value.map((item) => sanitizeValue(item, seen)) as T;
  if (typeof value === "object") {
    if (seen.has(value as object)) return value;
    seen.add(value as object);
    const record = value as Record<string, unknown>;
    for (const [key, entry] of Object.entries(record)) {
      record[key] = sanitizeValue(entry, seen);
    }
  }
  return value;
}

export function sanitizeEvent(event: Event, _hint?: EventHint): Event {
  const seen = new WeakSet<object>();
  if (event.user) {
    if (event.user.email) event.user.email = EMAIL_REDACTED;
    if (event.user.ip_address) delete event.user.ip_address;
  }
  if (event.request) {
    event.request.headers = sanitizeHeaders(event.request.headers) as
      | Record<string, string>
      | undefined;
    if (typeof event.request.query_string === "string") {
      event.request.query_string = sanitizeString(event.request.query_string);
    }
    if (typeof event.request.data === "string") {
      event.request.data = sanitizeString(event.request.data);
    }
  }
  if (event.contexts) event.contexts = sanitizeValue(event.contexts, seen);
  if (event.extra) event.extra = sanitizeValue(event.extra, seen);
  if (event.tags) event.tags = sanitizeValue(event.tags, seen);
  return event;
}

export function sanitizeBreadcrumb(breadcrumb: Breadcrumb): Breadcrumb | null {
  if (!breadcrumb) return breadcrumb;
  const seen = new WeakSet<object>();
  if (breadcrumb.data) breadcrumb.data = sanitizeValue(breadcrumb.data, seen);
  if (typeof breadcrumb.message === "string") {
    breadcrumb.message = sanitizeString(breadcrumb.message);
  }
  return breadcrumb;
}

function shouldEnable(dsn: string | undefined): boolean {
  if (!dsn) return false;
  if (process.env.NODE_ENV === "test") return false;
  if (process.env.NEXT_PUBLIC_DISABLE_SENTRY === "true") return false;
  return true;
}

function resolveDsn(target: SentryTarget): string | undefined {
  if (target === "client") {
    return process.env.NEXT_PUBLIC_SENTRY_DSN || process.env.SENTRY_DSN;
  }
  return process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;
}

function resolveEnvironment(): string | undefined {
  if (process.env.SENTRY_ENVIRONMENT) return process.env.SENTRY_ENVIRONMENT;
  const vercelEnv =
    process.env.VERCEL_ENV || process.env.NEXT_PUBLIC_VERCEL_ENV;
  if (vercelEnv === "production") return "production";
  if (vercelEnv === "preview") return "preview";
  if (vercelEnv === "development") return "development";
  return process.env.NODE_ENV;
}

function resolveRelease(): string | undefined {
  return (
    process.env.SENTRY_RELEASE ||
    process.env.VERCEL_GIT_COMMIT_SHA ||
    process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA ||
    process.env.npm_package_version
  );
}

export function createSentryOptions(target: SentryTarget): SentryInitOptions {
  const dsn = resolveDsn(target);
  const enabled = shouldEnable(dsn);
  const tracesSampleRate = parseSampleRate(
    process.env.SENTRY_TRACES_SAMPLE_RATE,
    0.1
  );

  const options: SentryInitOptions = {
    dsn,
    enabled,
    environment: resolveEnvironment(),
    release: resolveRelease(),
    tracesSampleRate,
    sendDefaultPii: false,
    beforeSend: (event: Event, hint?: EventHint) => sanitizeEvent(event, hint),
    beforeBreadcrumb: (breadcrumb: Breadcrumb) =>
      sanitizeBreadcrumb(breadcrumb),
  };

  if (target === "client") {
    options.replaysSessionSampleRate = parseSampleRate(
      process.env.SENTRY_REPLAYS_SESSION_SAMPLE_RATE,
      0
    );
    options.replaysOnErrorSampleRate = parseSampleRate(
      process.env.SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE,
      1.0
    );
  }

  if (!enabled) {
    options.tracesSampleRate = 0;
    options.replaysSessionSampleRate = 0;
    options.replaysOnErrorSampleRate = 0;
  }

  return options;
}
