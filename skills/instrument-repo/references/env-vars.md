# Environment Variables Reference

## Sentry

| Variable | Scope | Required | Notes |
|----------|-------|----------|-------|
| `NEXT_PUBLIC_SENTRY_DSN` | Per-project | Yes (Next.js) | Client-side accessible DSN |
| `SENTRY_DSN` | Per-project | Yes (server) | Server-side DSN |
| `SENTRY_AUTH_TOKEN` | Shared | For source maps | Org-level auth token |
| `SENTRY_ORG` | `misty-step` | Config | Hardcode in sentry config |
| `SENTRY_PROJECT` | Per-project | Config | Matches Sentry project slug |
| `SENTRY_TRACES_SAMPLE_RATE` | Per-project | No | Default 0.1 (10%) |
| `SENTRY_ENVIRONMENT` | Per-project | No | Auto-detected from Vercel |
| `SENTRY_RELEASE` | Per-project | No | Auto-detected from git SHA |

## PostHog

| Variable | Scope | Required | Notes |
|----------|-------|----------|-------|
| `NEXT_PUBLIC_POSTHOG_KEY` | Shared | Yes | Project API key (project 293836) |
| `NEXT_PUBLIC_POSTHOG_HOST` | Shared | No | Default `/ingest` via rewrite |

## Helicone

| Variable | Scope | Required | Notes |
|----------|-------|----------|-------|
| `HELICONE_API_KEY` | Shared | Yes (server) | Never expose client-side |

## .env.example Template (Next.js)

```bash
# Sentry — error tracking
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_AUTH_TOKEN=
SENTRY_ORG=misty-step
SENTRY_PROJECT=

# PostHog — product analytics
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=/ingest

# Helicone — LLM cost tracking (if applicable)
# HELICONE_API_KEY=
```

## .env.example Template (Go CLI)

```bash
# Sentry — error tracking
SENTRY_DSN=
```

## .env.example Template (Python)

```bash
# Sentry — error tracking
SENTRY_DSN=
```
