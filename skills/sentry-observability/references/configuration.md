# Sentry Configuration Patterns

Advanced configuration patterns for Sentry in Next.js applications.

## Clean Environment Naming

**Problem:** Vercel defaults to "vercel-production", "vercel-preview" (ugly in Sentry dashboard)

**Solution:** Override in shared Sentry config

```typescript
// lib/sentry.ts
function resolveEnvironment(): string | undefined {
  // Explicit override takes precedence
  if (process.env.SENTRY_ENVIRONMENT) {
    return process.env.SENTRY_ENVIRONMENT;
  }

  // Map Vercel environments to clean names
  const vercelEnv = process.env.VERCEL_ENV || process.env.NEXT_PUBLIC_VERCEL_ENV;
  if (vercelEnv === 'production') return 'production';
  if (vercelEnv === 'preview') return 'preview';
  if (vercelEnv === 'development') return 'development';

  return process.env.NODE_ENV;
}
```

**Result:** Sentry dashboard shows "production", "preview", "development"

## next.config.ts Options

```typescript
import { withSentryConfig } from '@sentry/nextjs';

const nextConfig = {
  // ... your Next.js config
};

const sentryNextConfigOptions = {
  silent: !process.env.CI,

  // Hide source maps from client bundles (security)
  hideSourceMaps: true,

  // Tree-shake Sentry logger in production (bundle size)
  disableLogger: true,
};

const sentryWebpackPluginOptions = {
  // Monitor Vercel Cron jobs automatically
  automaticVercelMonitors: true,

  // Source map upload
  authToken: process.env.SENTRY_AUTH_TOKEN,
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
};

export default withSentryConfig(
  nextConfig,
  sentryNextConfigOptions,
  sentryWebpackPluginOptions
);
```

## Sample Rate Configuration

### Performance Traces

```typescript
Sentry.init({
  tracesSampleRate: parseSampleRate(
    process.env.SENTRY_TRACES_SAMPLE_RATE,
    0.1 // 10% default
  ),
});
```

### Environment Variables

```bash
# .env.local or Vercel environment
SENTRY_TRACES_SAMPLE_RATE=0.1           # 10% of requests
SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0    # Disabled (cost-aware)
SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0 # 100% when errors occur
```

## Alert Automation (CLI)

Create version-controlled alerts via REST API:

```bash
#!/bin/bash
# scripts/configure-sentry-alerts.sh

SENTRY_API_BASE="https://sentry.io/api/0"

create_alert() {
  local name="$1"
  local payload="$2"

  curl -s -X POST \
    "${SENTRY_API_BASE}/projects/${SENTRY_ORG}/${SENTRY_PROJECT}/rules/" \
    -H "Authorization: Bearer ${SENTRY_API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

# Alert: New error types
create_alert "New Error Type" '{
  "name": "New Error Type",
  "actionMatch": "any",
  "filterMatch": "all",
  "frequency": 30,
  "conditions": [
    {"id": "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition"}
  ],
  "actions": [
    {
      "id": "sentry.mail.actions.NotifyEmailAction",
      "targetType": "IssueOwners",
      "fallthroughType": "ActiveMembers"
    }
  ]
}'
```

Or use the skill script:

```bash
~/.claude/skills/sentry-observability/scripts/create_alert.sh \
  --name "New Errors" \
  --type issue
```

## Cost Considerations

Free tier limits:
- 5,000 errors/month (~166/day)
- Session Replay counts toward quota

**Recommendations:**
- Start with 0% routine replay, 100% error-only
- Keep trace sample rate at 10% or lower
- Increase only when actively debugging
