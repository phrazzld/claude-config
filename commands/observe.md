---
description: Audit observability infrastructure and generate CLI-first improvement plan
---

Audit and improve observability infrastructure.

# OBSERVE

Systematically audit error tracking, performance monitoring, analytics, and logging infrastructure. Identify gaps, research modern patterns, generate actionable CLI-based improvements.

## The Observability-First Principle

*"You can't improve what you don't measure. You can't debug what you don't observe."*

Production systems without comprehensive observability are invisible failures waiting to happen. This command audits whether you have the instrumentation to:
- **Catch errors** before users report them
- **Debug production issues** without guessing
- **Understand user behavior** to drive product decisions
- **Optimize performance** with real data
- **Track deployments** and detect regressions

**Prefer CLI-manageable tools**: Version-controlled configs > manual dashboards. Infrastructure-as-code > click-ops.

---

## Phase 1: Detect Current Setup

### 1.1 Scan for Observability Tools

**Search codebase for:**
```bash
# Error tracking
package.json dependencies: @sentry/*, sentry-*, @bugsnag/*, rollbar, airbrake

# OpenTelemetry
package.json dependencies: @opentelemetry/*, @vercel/otel, spectacle

# Analytics
package.json dependencies: @vercel/analytics, @vercel/speed-insights, posthog-*, mixpanel, amplitude-*, plausible

# Logging
package.json dependencies: pino, winston, bunyan, @opentelemetry/instrumentation-pino

# APM/Tracing
package.json dependencies: dd-trace, newrelic, elastic-apm-node

# Monitoring
package.json dependencies: @grafana/*, prometheus-*
```

**Check configurations:**
```bash
# Sentry configs
Find: sentry.*.config.{ts,js}, instrumentation.ts with Sentry imports

# OpenTelemetry instrumentation
Find: instrumentation.ts, otel.config.{ts,js}, telemetry setup files

# Analytics integrations
Find: _app.tsx with analytics, middleware.ts with tracking, layout.tsx imports

# GitHub Actions observability
Find: .github/workflows/* with Sentry releases, deployment notifications

# CLI automation scripts
Find: scripts/*sentry*, scripts/*alert*, scripts/*grafana*, scripts/*observe*
```

### 1.2 Environment Variable Audit

**Search for observability env vars:**
```bash
# Check .env.example, .env.local, vercel.json, README
Grep for:
- SENTRY_DSN, SENTRY_AUTH_TOKEN, SENTRY_ORG, SENTRY_PROJECT
- OTEL_EXPORTER_OTLP_ENDPOINT, GRAFANA_CLOUD_*
- VERCEL_ANALYTICS_ID, NEXT_PUBLIC_ANALYTICS_*
- LOG_LEVEL, PINO_LOG_LEVEL

# Check Vercel environment variables (if applicable)
vercel env ls | grep -E "SENTRY|OTEL|ANALYTICS|GRAFANA"

# Check Convex environment (if using Convex backend)
npx convex env ls | grep -E "SENTRY|OTEL"
```

### 1.3 Deployment Integration Check

**GitHub integration status:**
```bash
# Check if Sentry releases are automated
gh workflow list | grep -i sentry
gh workflow view <workflow-name> | grep -i release

# Check deployment notifications
gh api repos/:owner/:repo/hooks | grep -E "sentry|grafana|slack"
```

---

## Phase 2: Deep Research

Use all available research tools to understand modern patterns for detected stack:

### 2.1 Web Search for Latest Patterns

**Research queries:**
```
WebSearch:
- "Vercel Analytics vs Sentry Performance 2025"
- "OpenTelemetry Next.js production setup 2025"
- "Sentry Session Replay cost optimization"
- "Grafana Cloud free tier intelligent sampling"
- "Vercel Speed Insights best practices"
- "CLI-based Sentry alert automation"
- "GitHub Actions observability monitoring"
```

### 2.2 Exa MCP for Technical Documentation

**Fetch docs for detected libraries:**
```
exa-code:
- "@sentry/nextjs configuration options"
- "@vercel/otel Grafana Cloud integration"
- "@vercel/analytics custom events API"
- "OpenTelemetry instrumentation-pino setup"
- "Next.js instrumentation.ts patterns"
```

### 2.3 Gemini CLI for Comparative Analysis

**Research questions:**
```
gemini --prompt:
- "Compare Sentry vs Datadog vs Grafana Cloud for Next.js error tracking"
- "Best practices for OpenTelemetry sampling in production"
- "How to implement cost-effective observability on free tiers"
- "PII redaction strategies for error tracking compliance"
- "CLI-first monitoring automation patterns"
```

---

## Phase 3: Gap Analysis

Evaluate across six observability dimensions:

### 3.1 Error Tracking (Sentry / Bugsnag / Rollbar)

**Audit checklist:**
- ✅ **Setup Quality**
  - [ ] Using Vercel Integration (not manual tokens)?
  - [ ] Clean environment naming ("production" not "vercel-production")?
  - [ ] Source maps uploading automatically?
  - [ ] Test error route exists (`/test-error` or similar)?

- ✅ **Security & Privacy**
  - [ ] PII redaction configured (`beforeSend`, `sendDefaultPii: false`)?
  - [ ] Email scrubbing active?
  - [ ] Authorization headers filtered?
  - [ ] IP addresses removed?
  - [ ] Source maps hidden from production bundle?

- ✅ **Alert Automation**
  - [ ] CLI-based alert configuration exists?
  - [ ] New error type alerts configured?
  - [ ] Error frequency spike alerts?
  - [ ] Version-controlled alert rules (scripts/)?

- ✅ **Cost Optimization**
  - [ ] Sample rates tuned (not 100% traces)?
  - [ ] Session Replay configured (0% routine, 100% error)?
  - [ ] Health check endpoints excluded?
  - [ ] Static asset requests filtered?

- ✅ **Backend Coverage**
  - [ ] Convex actions instrumented?
  - [ ] API routes tracked?
  - [ ] Serverless functions monitored?

**Red flags:**
- ❌ Manual token setup (will break on preview deploys)
- ❌ No PII redaction (compliance violation)
- ❌ Uncontrolled sample rates (quota exceeded)
- ❌ Manual alert clicking (not version-controlled)
- ❌ Errors only found via user reports (blind spots)

### 3.2 Performance Monitoring (OpenTelemetry / APM)

**Audit checklist:**
- ✅ **Trace Instrumentation**
  - [ ] OTLP exporter configured?
  - [ ] HTTP requests traced?
  - [ ] External API calls traced (fetch instrumentation)?
  - [ ] Database queries traced?
  - [ ] Custom business logic spans?

- ✅ **Sampling Strategy**
  - [ ] Intelligent sampler active (not naive random)?
  - [ ] 100% error trace capture?
  - [ ] Base rate appropriate (10-20% typical)?
  - [ ] Health checks excluded from sampling?
  - [ ] Custom URL patterns (high-value endpoints 100%)?

- ✅ **Backend Integration**
  - [ ] Convex actions export traces?
  - [ ] Trace context propagation (traceparent headers)?
  - [ ] Service mesh / multi-service tracing?

- ✅ **Visualization**
  - [ ] Grafana dashboards exist?
  - [ ] Latency percentiles tracked (p50, p99)?
  - [ ] Error rate visualizations?
  - [ ] Service dependency graphs?

**Red flags:**
- ❌ No tracing setup (flying blind on performance)
- ❌ 100% trace sampling (expensive, unnecessary)
- ❌ Missing trace context propagation (broken distributed traces)
- ❌ No performance baselines (can't detect regressions)

### 3.3 Analytics (Vercel Analytics / PostHog / Plausible)

**Audit checklist:**
- ✅ **User Analytics**
  - [ ] Vercel Analytics enabled?
  - [ ] Custom event tracking?
  - [ ] Conversion funnel measurement?
  - [ ] User journey analysis?

- ✅ **Performance Analytics**
  - [ ] Vercel Speed Insights active?
  - [ ] Core Web Vitals tracked?
  - [ ] Real User Monitoring (RUM)?

- ✅ **Privacy Compliance**
  - [ ] Cookie consent implemented?
  - [ ] Analytics respects DNT?
  - [ ] GDPR-compliant (if EU users)?

- ✅ **Product Insights**
  - [ ] Feature usage tracked?
  - [ ] A/B test instrumentation?
  - [ ] Drop-off point identification?

**Red flags:**
- ❌ No analytics (guessing at product decisions)
- ❌ Only server-side analytics (missing client behavior)
- ❌ Privacy violations (tracking without consent)
- ❌ Vanity metrics only (page views, not conversions)

### 3.4 Logging (Pino / Winston / Structured Logging)

**Audit checklist:**
- ✅ **Structured Logging**
  - [ ] JSON-formatted logs?
  - [ ] Consistent log levels (info, warn, error)?
  - [ ] Request ID / correlation ID?
  - [ ] Trace ID injection (OpenTelemetry integration)?

- ✅ **Log Aggregation**
  - [ ] Logs sent to centralized system (Grafana Loki, Datadog)?
  - [ ] Log retention policy?
  - [ ] Log-based alerting?

- ✅ **Development Experience**
  - [ ] Pretty-printed logs in dev (pino-pretty)?
  - [ ] Log filtering by level?
  - [ ] Sensitive data scrubbed (passwords, tokens)?

**Red flags:**
- ❌ console.log() everywhere (not queryable)
- ❌ Logs only in Vercel dashboard (disappear after 30 days)
- ❌ No correlation between logs and traces
- ❌ Secrets in logs (security issue)

### 3.5 Infrastructure Observability (CI/CD, Deployments, GitHub)

**Audit checklist:**
- ✅ **Deployment Tracking**
  - [ ] Sentry releases created on deploy?
  - [ ] Grafana annotations on deploy?
  - [ ] GitHub deployment events tracked?
  - [ ] Rollback detection?

- ✅ **CI/CD Monitoring**
  - [ ] GitHub Actions success rates tracked?
  - [ ] Build duration trends?
  - [ ] Test flakiness detection?
  - [ ] Deploy frequency / lead time metrics?

- ✅ **Health Checks**
  - [ ] `/health` or `/api/health` endpoint exists?
  - [ ] Uptime monitoring (UptimeRobot, BetterUptime)?
  - [ ] Synthetic checks from multiple regions?

**Red flags:**
- ❌ No deployment tracking (can't correlate errors with releases)
- ❌ Health checks missing (downtime detection delayed)
- ❌ GitHub Actions failures not monitored
- ❌ No rollback automation

### 3.6 Cost & Retention

**Audit checklist:**
- ✅ **Free Tier Utilization**
  - [ ] Sentry quota tracking (5k errors/month)?
  - [ ] Grafana Cloud limits known (10k series, 50GB traces)?
  - [ ] Sampling tuned to stay within free tier?

- ✅ **Data Retention**
  - [ ] Logs retention policy (7d? 30d?)?
  - [ ] Traces retention (24h? 7d?)?
  - [ ] Replay retention (30d?)?

- ✅ **Cost Alerts**
  - [ ] Quota usage monitoring?
  - [ ] Spend alerts configured?

**Red flags:**
- ❌ Exceeded free tier without realizing
- ❌ No retention policy (data lost or paying unnecessarily)
- ❌ Sampling too aggressive (missing critical data)

---

## Phase 4: Generate Recommendations

Based on gaps found, create prioritized improvements with exact CLI commands.

### Output Format

```markdown
## Observability Infrastructure Audit

**Project**: [detected project name]
**Stack**: [Next.js/React/Node/etc + detected tools]
**Audit Date**: [timestamp]

---

### 🔴 CRITICAL Gaps (Fix Immediately)

#### [Gap Name]
- **Current State**: [what's missing/broken]
- **Impact**: [user/business consequence]
- **Fix**: [exact CLI commands or code changes]
- **Effort**: [time estimate]
- **Priority**: CRITICAL

**Example:**
#### No PII Redaction in Sentry
- **Current State**: Raw user emails sent to Sentry (violates GDPR)
- **Impact**: Compliance violation, potential fines, user trust breach
- **Fix**:
  ```typescript
  // lib/sentry.ts
  export const sanitizeEvent = (event: Event): Event => {
    if (event.user?.email) event.user.email = '[EMAIL_REDACTED]';
    return event;
  };

  // sentry.client.config.ts
  Sentry.init({
    sendDefaultPii: false,
    beforeSend: (event) => sanitizeEvent(event),
  });
  ```
- **Effort**: 15 min
- **Priority**: CRITICAL

---

### 🟠 HIGH Priority (This Sprint)

#### [Gap Name]
- **Current State**: [description]
- **Impact**: [consequence]
- **Fix**: [CLI commands]
- **Effort**: [estimate]

**Example:**
#### No CLI-Based Alert Automation
- **Current State**: Alerts manually configured in Sentry dashboard
- **Impact**: Alert configs lost if workspace reset, no version control
- **Fix**:
  ```bash
  # Create scripts/configure-sentry-alerts.sh
  curl -X POST https://sentry.io/api/0/projects/$ORG/$PROJECT/rules/ \
    -H "Authorization: Bearer $SENTRY_API_TOKEN" \
    -d '{
      "name": "New Error Type",
      "conditions": [{"id": "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition"}],
      "actions": [{"id": "sentry.mail.actions.NotifyEmailAction"}]
    }'
  ```
  Commit script to repo, run on new environments
- **Effort**: 30 min

---

### 🟡 MEDIUM Priority (This Quarter)

[Same format as above, for lower-priority improvements]

---

### 🟢 LOW Priority (Nice to Have)

[Same format as above, for polish items]

---

## Generated TODOs (Ready for BACKLOG.md)

- [ ] [CRITICAL] Add PII redaction to Sentry config (15m)
- [ ] [HIGH] Create CLI-based alert automation script (30m)
- [ ] [HIGH] Enable Vercel Analytics + Speed Insights (5m)
- [ ] [MEDIUM] Set up Grafana dashboard for API latency (2h)
- [ ] [MEDIUM] Add OpenTelemetry trace context to Convex (1h)
- [ ] [LOW] Configure Session Replay with 5% sampling (10m)

---

## Research Summary

**Key Findings from Research:**
- [Insight from WebSearch about industry patterns]
- [Insight from Exa MCP about library capabilities]
- [Insight from Gemini about tool comparisons]

**Recommended Stack for This Project:**
- Error Tracking: [Tool + rationale]
- Performance Monitoring: [Tool + rationale]
- Analytics: [Tool + rationale]
- Logging: [Tool + rationale]

**Cost Estimate:**
- Current monthly cost: $X (or "free tier")
- Projected with improvements: $Y
- Free tier headroom: [X% of limits used]

---

## Quick Wins (< 30 min)

1. **[Action]**: [One-line description]
   ```bash
   [exact command]
   ```

2. **[Action]**: [One-line description]
   ```bash
   [exact command]
   ```

[Continue for all sub-30-minute improvements]

---

## Next Steps

1. **Immediate**: Fix CRITICAL gaps (estimated: [total time])
2. **This Week**: Implement HIGH priority items
3. **This Month**: Tackle MEDIUM priority improvements
4. **Ongoing**: Monitor quotas, tune sample rates, review dashboards

**Success Criteria:**
- ✅ All errors surfaced before user reports
- ✅ p99 latency < [target]ms tracked
- ✅ Cost within free tier (or < $X/month)
- ✅ All observability configs in version control
- ✅ Deployment-correlated error tracking active
```

---

## Philosophy

**Invisible Systems Stay Broken**: Production without observability = debugging by intuition. Instruments before incidents.

**CLI Over Dashboard**: `scripts/configure-alerts.sh` > clicking. Version control > tribal knowledge.

**Cost-Conscious Observability**: Free tiers (Sentry 5k errors, Grafana 10k series) handle most startups. Intelligent sampling > naive 100%.

**Privacy First**: PII redaction not negotiable. `[EMAIL_REDACTED]` > compliance fines.

**Correlation is Key**: Traces ↔ logs ↔ errors ↔ deployments. Isolated tools = context-free debugging.

**Automate Releases**: Sentry releases on deploy. Grafana annotations on deploy. GitHub deployment events tracked. Every deploy = observability checkpoint.

---

## Anti-Patterns to Detect

### ❌ Observability Theater
**Symptom**: Tools installed but not configured / not used
**Detection**: Dependencies present, no env vars / dashboards unused
**Fix**: Remove unused tools or configure properly

### ❌ Manual Dashboard Configuration
**Symptom**: Alerts/dashboards created by clicking
**Detection**: No `scripts/` automation, tribal knowledge
**Fix**: Export configs, create CLI scripts, commit to repo

### ❌ 100% Sampling Everywhere
**Symptom**: Sentry tracesSampleRate=1.0, OTLP base sampling 100%
**Detection**: High quota usage, no sampling strategy
**Fix**: Implement intelligent sampler (10% base, 100% errors)

### ❌ No Error -> Deploy Correlation
**Symptom**: Can't tell which deploy introduced error
**Detection**: No Sentry releases, no Grafana annotations
**Fix**: Automate release creation in CI/CD

### ❌ Logs-Only Error Tracking
**Symptom**: Grepping Vercel logs for errors
**Detection**: No Sentry/error tracker, console.log() debugging
**Fix**: Install proper error tracker with stack traces

### ❌ Analytics-Free Product
**Symptom**: Product decisions by gut feel
**Detection**: No Vercel Analytics, no event tracking
**Fix**: Enable Vercel Analytics + custom events

---

## Tool Decision Trees

### Should I use Sentry or Grafana for errors?

```
Do you need Session Replay (visual debugging)?
├─ YES → Sentry (session replay built-in)
│
└─ NO → Are you already using Grafana Cloud for traces?
    ├─ YES → Grafana (unified observability)
    └─ NO → Sentry (easier setup, Vercel Integration)
```

### Should I use OpenTelemetry or Sentry Performance?

```
Do you need custom business metrics (orders/sec, cache hits)?
├─ YES → OpenTelemetry (flexible metrics)
│
└─ NO → Are you on Vercel?
    ├─ YES → Sentry Performance (Vercel Integration, simpler)
    └─ NO → OpenTelemetry (vendor-neutral, future-proof)
```

### Should I use Vercel Analytics or PostHog?

```
Do you need feature flags, A/B testing, or session recording?
├─ YES → PostHog (full product analytics suite)
│
└─ NO → Are you on Vercel?
    ├─ YES → Vercel Analytics (zero-config, privacy-first)
    └─ NO → Plausible (privacy-first alternative)
```

---

## Quick Reference: CLI Commands

### Sentry

```bash
# Check Vercel Integration status
vercel env ls | grep SENTRY

# Test error capture
curl https://your-app.vercel.app/test-error

# Create alert via CLI
curl -X POST https://sentry.io/api/0/projects/$ORG/$PROJECT/rules/ \
  -H "Authorization: Bearer $SENTRY_API_TOKEN" \
  -d '{"name": "New Errors", "conditions": [...], "actions": [...]}'

# List existing alerts
curl -H "Authorization: Bearer $SENTRY_API_TOKEN" \
  https://sentry.io/api/0/projects/$ORG/$PROJECT/rules/

# Configure Convex backend
npx convex env set SENTRY_DSN "https://...@sentry.io/123" --prod
```

### OpenTelemetry / Grafana

```bash
# Check Grafana Cloud env vars
vercel env ls | grep GRAFANA

# Test OTLP endpoint
curl -X POST https://otlp-gateway-prod-us-east-0.grafana.net/otlp/v1/traces \
  -H "Authorization: Basic $(echo -n "$GRAFANA_INSTANCE_ID:$GRAFANA_API_KEY" | base64)" \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[]}'

# View recent traces (if Grafana CLI configured)
grafana-cli traces query --from=-1h

# Check spectacle library version
npm list spectacle
```

### Vercel Analytics

```bash
# Enable analytics
vercel env add VERCEL_ANALYTICS_ID

# Enable Speed Insights
npm install @vercel/speed-insights
# Add to app/layout.tsx: <SpeedInsights />

# View analytics CLI (limited, prefer dashboard)
vercel analytics --from=7d
```

### GitHub

```bash
# Check deployment tracking
gh api repos/:owner/:repo/deployments | jq '.[] | {id, environment, created_at}'

# Check workflow runs
gh run list --workflow=deploy.yml --limit 10

# Check if Sentry GitHub integration active
gh api repos/:owner/:repo/hooks | jq '.[] | select(.config.url | contains("sentry"))'
```

---

## Checklist: Comprehensive Observability

Use this as final validation:

**Error Tracking**
- [ ] Sentry (or equivalent) installed
- [ ] Vercel Integration configured (not manual tokens)
- [ ] PII redaction active
- [ ] Source maps uploading
- [ ] Alert automation via CLI
- [ ] Test error route verified
- [ ] Backend (Convex/API) covered

**Performance Monitoring**
- [ ] OpenTelemetry SDK initialized
- [ ] Intelligent sampler (10% base, 100% error)
- [ ] HTTP/fetch instrumentation active
- [ ] Trace context propagates to backend
- [ ] Grafana dashboards created
- [ ] p99 latency < [target]ms

**Analytics**
- [ ] Vercel Analytics enabled
- [ ] Speed Insights installed
- [ ] Custom events tracked
- [ ] Conversion funnels defined
- [ ] Privacy-compliant (cookie consent)

**Logging**
- [ ] Structured logging (JSON)
- [ ] Trace ID injection
- [ ] Centralized aggregation
- [ ] Retention policy set
- [ ] PII scrubbed from logs

**Infrastructure**
- [ ] Deployment tracking (Sentry releases)
- [ ] Health check endpoint
- [ ] Uptime monitoring
- [ ] CI/CD observability
- [ ] Rollback automation

**Cost & Governance**
- [ ] Free tier limits known
- [ ] Quota monitoring active
- [ ] Sampling tuned
- [ ] Retention policies set
- [ ] All configs version-controlled

---

*Run this command when setting up new projects or quarterly audits of existing observability infrastructure.*
