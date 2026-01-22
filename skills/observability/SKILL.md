---
name: observability
description: |
  Complete observability infrastructure. Error tracking, alerting, logging, health checks.
  Optimized for indie dev: minimal services, CLI-manageable, AI agent integration.
argument-hint: "[focus area, e.g. 'alerts' or 'health checks']"
---

# /observability

Production observability with one service. Audit, fix, verify—every time.

## Philosophy

**One service, not twenty.** Sentry handles errors. Vercel handles logs. That's it.

**CLI-first.** Everything manageable from command line. No dashboard clicking.

**AI-agent ready.** Errors should trigger automated analysis and fixes.

## What This Does

Examines project observability, identifies gaps, implements fixes, and verifies alerting works. Every run does the full cycle.

## Architecture

```
App → Sentry (errors, performance)
    → stdout (Vercel captures automatically)
    → /api/health (uptime monitoring)

AI Integration:
    Sentry MCP → Claude (query errors, analyze, fix)
    Sentry webhook → GitHub Action → agent (auto-triage)
    CLI scripts → manual triage and resolution
```

**Services:** 1 (Sentry)
**Built-in free:** Vercel logs, Vercel Analytics
**CLI-manageable:** 100%

## Process

### 1. Audit

**Check what exists:**
```bash
# Sentry configured?
~/.claude/skills/sentry-observability/scripts/detect_sentry.sh

# Health endpoint?
[ -f "app/api/health/route.ts" ] || [ -f "src/app/api/health/route.ts" ] && echo "✓ Health endpoint" || echo "✗ Health endpoint"

# Structured logging?
grep -r "console.log\|console.error" --include="*.ts" --include="*.tsx" src/ app/ 2>/dev/null | head -5

# Vercel Analytics?
grep -q "@vercel/analytics" package.json && echo "✓ Vercel Analytics" || echo "✗ Vercel Analytics"
```

**Spawn agent for deep review:**
Spawn `observability-advocate` agent to audit logging coverage, error handling, and silent failure risks.

### 2. Plan

Every project needs:

**Essential (every production app):**
- Sentry error tracking with source maps
- Health check endpoint (`/api/health`)
- Structured logging (JSON to stdout)
- At least one alert rule (new errors)

**Recommended:**
- Vercel Analytics (free, zero config)
- Webhook for AI agent integration
- Triage scripts for CLI management

**Only if needed:**
- PostHog (if you need product analytics)
- Custom uptime monitoring

### 3. Execute

**Install Sentry:**
```bash
pnpm add @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

Or use init script:
```bash
~/.claude/skills/sentry-observability/scripts/init_sentry.sh
```

**Configure PII redaction:**
```typescript
// sentry.client.config.ts
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  beforeSend(event) {
    // Scrub PII
    if (event.extra) delete event.extra.password;
    if (event.user) delete event.user.email;
    return event;
  },
});
```

**Create health endpoint:**
```typescript
// app/api/health/route.ts
export async function GET() {
  const checks = {
    app: 'ok',
    timestamp: new Date().toISOString(),
  };

  // Add service checks as needed
  // checks.database = await checkDb();
  // checks.stripe = await checkStripe();

  return Response.json(checks);
}
```

**Add Vercel Analytics (optional but free):**
```bash
pnpm add @vercel/analytics
```

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

**Set up structured logging:**
Use JSON logs that Vercel can parse:
```typescript
// lib/logger.ts
export function log(level: 'info' | 'warn' | 'error', message: string, data?: Record<string, unknown>) {
  const entry = {
    level,
    message,
    timestamp: new Date().toISOString(),
    ...data,
  };
  console[level === 'error' ? 'error' : 'log'](JSON.stringify(entry));
}
```

**Create alert rule:**
```bash
~/.claude/skills/sentry-observability/scripts/create_alert.sh --name "New Errors" --type issue
```

**Set up webhook for AI integration (optional):**
In Sentry Dashboard → Settings → Integrations → Internal Integrations:
1. Create integration with webhook URL
2. Subscribe to issue events
3. Point to GitHub Action or custom endpoint

### 4. Verify

**Verify Sentry setup:**
```bash
~/.claude/skills/sentry-observability/scripts/verify_setup.sh
```

**Test error tracking:**
```typescript
// Trigger test error
throw new Error('Test error for Sentry verification');
```

Then check Sentry dashboard or:
```bash
~/.claude/skills/sentry-observability/scripts/list_issues.sh --limit 1
```

**Test health endpoint:**
```bash
curl -s http://localhost:3000/api/health | jq
```

**Test alerting:**
- Trigger an error
- Verify alert fires (check email/Slack/webhook)

If any verification fails, go back and fix it.

## AI Agent Integration

### Option A: Sentry MCP Server

For direct Claude integration, use the Sentry MCP server:
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@anthropic/sentry-mcp"],
      "env": {
        "SENTRY_AUTH_TOKEN": "your-token",
        "SENTRY_ORG": "your-org"
      }
    }
  }
}
```

Claude can then:
- Query recent errors
- Get full error context
- Analyze root causes
- Propose fixes

### Option B: Webhook → GitHub Action → Agent

For automated triage:
```yaml
# .github/workflows/sentry-triage.yml
name: Sentry Auto-Triage

on:
  repository_dispatch:
    types: [sentry-issue]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Analyze with Claude
        run: |
          # Query issue details and spawn analysis agent
          claude --print "Analyze Sentry issue ${{ github.event.client_payload.issue_id }}"
```

### Option C: CLI Scripts (Already Exist)

```bash
# List and triage issues
~/.claude/skills/sentry-observability/scripts/list_issues.sh --env production
~/.claude/skills/sentry-observability/scripts/triage_score.sh --json

# Get issue details for analysis
~/.claude/skills/sentry-observability/scripts/issue_detail.sh PROJ-123

# Resolve after fixing
~/.claude/skills/sentry-observability/scripts/resolve_issue.sh PROJ-123
```

## Tool Choices

**Sentry over alternatives.** Best error tracking, mature CLI, AI-first roadmap (Seer webhooks, auto-fix features), excellent free tier.

**Vercel logs over log services.** stdout is captured automatically. No additional service needed. Query with `vercel logs`.

**Vercel Analytics over PostHog/Plausible.** Free with Vercel, zero config. Add PostHog only if you need product analytics (funnels, cohorts, feature flags).

## Environment Variables

```bash
# .env.example

# Sentry (required for error tracking)
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_AUTH_TOKEN=
SENTRY_ORG=
SENTRY_PROJECT=
```

## What You Get

When complete:
- Sentry capturing all errors with source maps
- Health check endpoint at `/api/health`
- Structured JSON logging (captured by Vercel)
- At least one alert rule configured
- Vercel Analytics for web vitals (optional)
- AI agent integration ready (MCP or webhooks)

User can:
- See errors in Sentry immediately when they occur
- Get alerted on new/critical errors
- Query errors via CLI (`list_issues.sh`, `triage_score.sh`)
- Trigger AI analysis of errors
- Monitor app health via `/api/health`
- View logs via `vercel logs`

## Related Skills

- `sentry-observability` — Detailed Sentry setup and scripts
- `observability-stack` — PostHog/analytics integration patterns
- `observability-advocate` — Agent for auditing observability coverage
