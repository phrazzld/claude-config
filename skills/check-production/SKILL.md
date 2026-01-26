---
name: check-production
description: |
  Check production health: Sentry errors, Vercel logs, health endpoints.
  Outputs structured findings. Use log-production-issues to create issues.
  Invoke for: production diagnostics, error audit, health status.
---

# /check-production

Audit production health. Output findings as structured report.

## What This Does

1. Query Sentry for unresolved issues
2. Check Vercel logs for recent errors
3. Test health endpoints
4. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-production-issues` to create GitHub issues or `/triage` to fix.

## Process

### 1. Sentry Check

```bash
# Run triage script if available
~/.claude/skills/triage/scripts/check_sentry.sh 2>/dev/null || echo "Sentry check unavailable"
```

Or spawn Sentry MCP query if configured.

### 2. Vercel Logs Check

```bash
# Check for recent errors
~/.claude/skills/triage/scripts/check_vercel_logs.sh 2>/dev/null || vercel logs --output json 2>/dev/null | head -50
```

### 3. Health Endpoints

```bash
# Test health endpoint
~/.claude/skills/triage/scripts/check_health_endpoints.sh 2>/dev/null || curl -sf "$(grep NEXT_PUBLIC_APP_URL .env.local 2>/dev/null | cut -d= -f2)/api/health" | jq .
```

### 4. Quick Application Checks

```bash
# Check for error handling gaps
grep -rE "catch\s*\(\s*\)" --include="*.ts" --include="*.tsx" src/ app/ 2>/dev/null | head -5
# Empty catch blocks = silent failures
```

## Output Format

```markdown
## Production Health Check

### P0: Critical (Active Production Issues)
- [SENTRY-123] PaymentIntent failed - 23 users affected (Score: 147)
  Location: api/checkout.ts:45
  First seen: 2h ago

### P1: High (Degraded Performance)
- Health endpoint slow: /api/health responding in 2.3s (should be <500ms)
- Vercel logs show 5xx errors in last hour (count: 12)

### P2: Medium (Warnings)
- 3 empty catch blocks found (silent failures)
- Health endpoint missing database connectivity check

### P3: Low (Improvements)
- Consider adding Sentry performance monitoring
- Health endpoint could include more service checks

## Summary
- P0: 1 | P1: 2 | P2: 2 | P3: 2
- Recommendation: Fix P0 immediately, then address P1s
```

## Priority Mapping

| Signal | Priority |
|--------|----------|
| Active errors affecting users | P0 |
| 5xx errors, slow responses | P1 |
| Silent failures, missing checks | P2 |
| Missing monitoring, improvements | P3 |

## Analytics Note

This skill checks production health (errors, logs, endpoints), not product analytics.

For analytics auditing, see `/check-observability`. Note:
- **PostHog** is REQUIRED for product analytics (has MCP server)
- **Vercel Analytics** is NOT acceptable (no CLI/API/MCP - unusable for our workflow)

If you need to investigate user behavior or funnels during incident response, query PostHog via MCP.

## Related

- `/log-production-issues` - Create GitHub issues from findings
- `/triage` - Fix production issues
- `/observability` - Set up monitoring infrastructure
