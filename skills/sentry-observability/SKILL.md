---
name: sentry-observability
description: |
  Apply modern Sentry observability patterns for Next.js applications:
  Vercel Integration setup, clean environment naming, Session Replay, PII redaction,
  CLI-based alert automation, and production-ready error tracking. Use when setting up
  Sentry, configuring observability, writing error handling, or reviewing monitoring setup.
---

# Sentry Observability

Modern error tracking and observability for Next.js applications deployed to Vercel.

## When to Use This Skill

- Setting up Sentry for new Next.js projects
- Configuring Session Replay and performance monitoring
- Implementing PII-safe error tracking
- Creating CLI-based alert automation
- Troubleshooting source map upload issues
- Reviewing observability configuration
- Implementing test error routes

## Core Principles

1. **Vercel Integration First**: Use marketplace integration, not manual token setup
2. **Clean Environments**: Override "vercel-production" to just "production"
3. **Security by Default**: Aggressive PII redaction, hide source maps
4. **CLI Automation**: Version-controlled alerts via REST API
5. **Cost Awareness**: Tune sample rates to avoid free tier limits
6. **Test Everything**: Dedicated error routes for verification

## Setup Patterns

### ✅ Recommended: Vercel Integration (2025 Best Practice)

**Why**: Auto-creates auth token, eliminates release ID mismatches, automatic source map upload

```bash
# 1. Install Vercel Integration
# Visit: https://vercel.com/integrations/sentry
# Click "Add Integration" → Select your project

# 2. Verify environment variables created automatically
vercel env ls | grep SENTRY

# Expected:
# SENTRY_AUTH_TOKEN (production, preview)
# NEXT_PUBLIC_SENTRY_DSN (production, preview)
# SENTRY_ORG (all environments)
# SENTRY_PROJECT (all environments)

# 3. Copy DSN to .env.local for development
echo "NEXT_PUBLIC_SENTRY_DSN=<your-dsn>" >> .env.local
echo "SENTRY_DSN=<your-dsn>" >> .env.local

# 4. For backend errors (Convex, API routes, etc.)
# Set SENTRY_DSN in backend environment
# Convex: npx convex env set SENTRY_DSN "<your-dsn>" --prod
```

**Benefits**:
- ✅ Zero manual token management
- ✅ Automatic source map upload on every deploy
- ✅ Release tracking with correct git SHA
- ✅ No "release not found" errors
- ✅ Works with Vercel preview deployments

### ❌ Anti-Pattern: Manual Auth Token Setup

```bash
# AVOID: Manual token creation and environment variable setup
# Problems:
# - Release ID mismatches between frontend and backend
# - Token rotation requires manual updates
# - No automatic source map upload
# - Preview deployments break
```

**Only use manual setup if**:
- Self-hosting (not using Vercel)
- Organization security policy prevents integrations
- Need fine-grained token permissions

## Configuration Patterns

### Clean Environment Naming

**Problem**: Vercel defaults to "vercel-production", "vercel-preview" (ugly in Sentry dashboard)

**Solution**: Override in shared Sentry config

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

export function createSentryOptions(target: 'client' | 'server' | 'edge') {
  return {
    dsn: resolveDsn(target),
    environment: resolveEnvironment(),
    // ... other options
  };
}
```

**Result**: Sentry dashboard shows "production", "preview", "development" instead of "vercel-*"

### Modern next.config.ts Options

```typescript
// next.config.ts
import { withSentryConfig } from '@sentry/nextjs';

const nextConfig = {
  // ... your Next.js config
};

const sentryNextConfigOptions = {
  silent: !process.env.CI,

  // ✅ Hide source maps from generated client bundles (security)
  hideSourceMaps: true,

  // ✅ Tree-shake Sentry logger in production (reduces bundle size)
  disableLogger: true,
};

const sentryWebpackPluginOptions = {
  // ✅ Monitor Vercel Cron jobs automatically
  automaticVercelMonitors: true,

  // Upload source maps during build
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

### Session Replay Configuration

**What it does**: Records user interactions before errors for visual debugging

```typescript
// lib/sentry.ts
export function createSentryOptions(target: 'client' | 'server' | 'edge') {
  const options = {
    // ... base options
  };

  if (target === 'client') {
    // ✅ Routine session recording (cost-aware default: 0%)
    options.replaysSessionSampleRate = parseSampleRate(
      process.env.SENTRY_REPLAYS_SESSION_SAMPLE_RATE,
      0
    );

    // ✅ Always record when errors occur (default: 100%)
    options.replaysOnErrorSampleRate = parseSampleRate(
      process.env.SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE,
      1.0
    );
  }

  return options;
}
```

**Environment variables**:
```bash
# .env.local or Vercel environment
SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0.05    # 5% of normal sessions
SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0   # 100% of error sessions
```

**Cost considerations**:
- Free tier: 5,000 errors/month (~166/day)
- Session Replay counts toward quota
- Start with 0% routine, 100% error-only
- Increase routine sampling only if needed for UX debugging

### PII Redaction (Security Critical)

**Required**: Automatically scrub sensitive data from all events

```typescript
// lib/sentry.ts
const EMAIL_REDACTION_PATTERN = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const EMAIL_REDACTED = '[EMAIL_REDACTED]';
const SENSITIVE_HEADERS = new Set(['authorization', 'cookie', 'set-cookie', 'x-api-key']);

export function sanitizeEvent(event: Event, _hint?: EventHint): Event {
  // Redact user email
  if (event.user?.email) {
    event.user.email = EMAIL_REDACTED;
  }

  // Remove IP address
  if (event.user?.ip_address) {
    delete event.user.ip_address;
  }

  // Sanitize headers
  if (event.request) {
    event.request.headers = sanitizeHeaders(event.request.headers);
  }

  // Recursively sanitize contexts, extra, tags
  // ... (see full implementation)

  return event;
}

export function createSentryOptions(target: SentryTarget) {
  return {
    sendDefaultPii: false,
    beforeSend: (event, hint) => sanitizeEvent(event, hint),
    beforeBreadcrumb: (breadcrumb) => sanitizeBreadcrumb(breadcrumb),
  };
}
```

**What gets redacted**:
- ✅ User emails → `[EMAIL_REDACTED]`
- ✅ IP addresses → deleted
- ✅ Authorization headers → deleted
- ✅ Cookies → deleted
- ✅ API keys → deleted

## Alert Automation

### CLI-Based Alert Configuration

**Why**: Version-controlled, repeatable, no manual clicking

**Setup**:
```bash
# 1. Create Sentry API token (one time)
# Visit: https://sentry.io/settings/account/api/auth-tokens/
# Scopes: project:write, alerts:write

# 2. Add to .env.local
echo "SENTRY_API_TOKEN=sntrys_xxx" >> .env.local

# 3. Create scripts/configure-sentry-alerts.sh
```

**Example script**:
```bash
#!/bin/bash
set -e

SENTRY_ORG="your-org"
SENTRY_PROJECT="your-project"
SENTRY_API_BASE="https://sentry.io/api/0"

# Load token
if [ -z "$SENTRY_API_TOKEN" ]; then
  if [ -f .env.local ]; then
    export SENTRY_API_TOKEN=$(grep "^SENTRY_API_TOKEN=" .env.local | cut -d= -f2 | tr -d '"')
  fi
fi

if [ -z "$SENTRY_API_TOKEN" ]; then
  echo "❌ Error: SENTRY_API_TOKEN not found"
  exit 1
fi

create_alert() {
  local name="$1"
  local payload="$2"

  response=$(curl -s -w "\n%{http_code}" -X POST \
    "${SENTRY_API_BASE}/projects/${SENTRY_ORG}/${SENTRY_PROJECT}/rules/" \
    -H "Authorization: Bearer ${SENTRY_API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | sed '$d')

  if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
    rule_id=$(echo "$body" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "✅ Created: $name (ID: $rule_id)"
  else
    echo "❌ Failed: $name (HTTP $http_code)"
    echo "   Response: $body"
  fi
}

# Alert: New error types
create_alert "New Error Type (All Environments)" '{
  "name": "New Error Type (All Environments)",
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

**Run**:
```bash
chmod +x scripts/configure-sentry-alerts.sh
./scripts/configure-sentry-alerts.sh
```

## Testing Patterns

### Test Error Route (Required)

**Why**: Verify Sentry captures errors before production

```typescript
// app/test-error/route.ts
import { NextRequest } from 'next/server';
import * as Sentry from '@sentry/nextjs';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const type = searchParams.get('type') || 'generic';

  // Add context for debugging
  Sentry.setContext('test_error', {
    type,
    timestamp: new Date().toISOString(),
    environment: process.env.VERCEL_ENV || 'development',
  });

  switch (type) {
    case 'generic':
      throw new Error('Test error - Sentry integration check');

    case 'async':
      await Promise.reject(new Error('Test async error'));
      break;

    case 'handled':
      try {
        throw new Error('Test handled error');
      } catch (error) {
        Sentry.captureException(error);
        return Response.json({ error: 'Handled error sent to Sentry' }, { status: 500 });
      }

    default:
      throw new Error(`Test error - Unknown type: ${type}`);
  }
}
```

**Usage**:
```bash
# Local testing
curl http://localhost:3000/test-error

# Preview deployment
curl https://your-branch-preview.vercel.app/test-error?type=async

# Production (use sparingly)
curl https://your-app.com/test-error?type=handled
```

**Verification**:
1. Check Sentry dashboard (Issues tab)
2. Verify environment name is clean ("production" not "vercel-production")
3. Verify source maps show original TypeScript code
4. Verify email alert received (if configured)
5. Check Session Replay attached (if error sampling enabled)

## Anti-Patterns Scanner

### ❌ Manual Environment Naming

```typescript
// BAD: Hardcoded environment strings
Sentry.init({
  environment: 'production', // Will be wrong in preview deployments
});
```

**Fix**: Use dynamic resolution
```typescript
// GOOD: Dynamic environment from Vercel
Sentry.init({
  environment: resolveEnvironment(), // Adapts to VERCEL_ENV
});
```

### ❌ No PII Redaction

```typescript
// BAD: Sending raw user data
Sentry.setUser({
  email: user.email, // Violates privacy regulations
  ip_address: request.ip,
});
```

**Fix**: Use sanitization hooks
```typescript
// GOOD: Automatic redaction
Sentry.init({
  sendDefaultPii: false,
  beforeSend: (event) => sanitizeEvent(event),
});
```

### ❌ Source Maps in Production Bundle

```typescript
// BAD: Exposes source code to users
const nextConfig = {
  productionBrowserSourceMaps: true, // Security risk
};
```

**Fix**: Hide from bundle, upload separately
```typescript
// GOOD: Source maps only in Sentry
const sentryOptions = {
  hideSourceMaps: true, // Not in bundle
};
```

### ❌ Uncontrolled Sample Rates

```typescript
// BAD: Default 100% tracing (expensive)
Sentry.init({
  tracesSampleRate: 1.0, // Will exceed free tier quickly
});
```

**Fix**: Environment-based tuning
```typescript
// GOOD: Configurable via env vars
const tracesSampleRate = parseSampleRate(
  process.env.SENTRY_TRACES_SAMPLE_RATE,
  0.1 // 10% default
);
```

## Decision Trees

### Session Replay: Should I Enable It?

```
Do you need visual debugging of user interactions?
├─ NO → Set SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0
│        SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0 (error-only)
│
└─ YES → Are you within free tier (5k errors/month)?
    ├─ YES → Start with SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0.05 (5%)
    │         SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0
    │
    └─ NO → Are you debugging a specific UX issue?
        ├─ YES → Temporarily increase to 0.5 (50%) during debug
        └─ NO → Lower to 0.01 (1%) or disable (0)
```

### Alert Configuration: CLI or Dashboard?

```
Do you need version-controlled alerts across environments?
├─ YES → Use CLI-based REST API approach
│         - Create scripts/configure-sentry-alerts.sh
│         - Store SENTRY_API_TOKEN in .env.local
│         - Commit script to repository
│
└─ NO → Are you creating metric alerts (error rate, performance)?
    ├─ YES → Use Sentry dashboard (metric alerts have different API)
    │         Navigate to: Alerts → Create Alert → Number of Errors
    │
    └─ NO → Use CLI for issue alerts (new errors, frequency spikes)
```

## Quick Reference

### Essential Environment Variables

```bash
# Frontend (Vercel)
NEXT_PUBLIC_SENTRY_DSN=https://...@o0.ingest.sentry.io/0
SENTRY_DSN=https://...@o0.ingest.sentry.io/0        # Server-side
SENTRY_AUTH_TOKEN=sntrys_...                         # Auto-set by Integration
SENTRY_ORG=your-org                                  # Auto-set by Integration
SENTRY_PROJECT=your-project                          # Auto-set by Integration

# Optional tuning
SENTRY_TRACES_SAMPLE_RATE=0.1                       # Performance traces (10%)
SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0.05             # Routine replays (5%)
SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0             # Error replays (100%)

# Backend (Convex, API routes, etc.)
SENTRY_DSN=https://...@o0.ingest.sentry.io/0

# CLI operations
SENTRY_API_TOKEN=sntrys_...                          # For alert automation
```

### Common Commands

```bash
# Verify Vercel Integration
vercel env ls | grep SENTRY

# Test error locally
curl http://localhost:3000/test-error

# Test preview deployment
curl https://your-preview.vercel.app/test-error

# Configure alerts via CLI
./scripts/configure-sentry-alerts.sh

# Check alert rules
curl -H "Authorization: Bearer $SENTRY_API_TOKEN" \
  https://sentry.io/api/0/projects/your-org/your-project/rules/

# Manual backend configuration (Convex example)
npx convex env set SENTRY_DSN "https://...@o0.ingest.sentry.io/0" --prod
```

### Troubleshooting

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Minified stack traces | Source maps not uploading | Install Vercel Integration |
| Errors not appearing | DSN mismatch | Verify DSN in both .env.local and deployment |
| "release not found" | Manual token setup | Switch to Vercel Integration |
| High quota usage | Excessive sampling | Lower sample rates |
| Session Replay not working | Sample rate = 0 | Set SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0 |
| Email alerts not working | Alert not configured | Run scripts/configure-sentry-alerts.sh |

## Philosophy

**Observability Is Not Optional**: Production errors without observability = invisible failures

**Security First**: PII redaction is not negotiable. Privacy violations >> lost debugging info

**Cost Awareness**: Free tier (5k errors/month) is enough for most projects. Tune sample rates before paying.

**CLI Over Dashboard**: Version-controlled alert rules > manual clicking. Treat observability as code.

**Test In Preview**: Never deploy Sentry to production without testing in preview deployment first.

**Clean Environments**: "production" > "vercel-production". Small details matter for maintainability.
