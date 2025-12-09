---
description: Audit observability infrastructure and generate CLI-first improvement plan
---

Audit and improve observability infrastructure.

# OBSERVE

Systematically audit error tracking, performance monitoring, analytics, and logging. Identify gaps, research modern patterns, generate actionable improvements.

## The Observability-First Principle

*"You can't improve what you don't measure. You can't debug what you don't observe."*

Production systems without comprehensive observability are invisible failures waiting to happen. This command audits whether you have instrumentation to:
- **Catch errors** before users report them
- **Debug production issues** without guessing
- **Understand user behavior** to drive product decisions
- **Optimize performance** with real data
- **Track deployments** and detect regressions

**Prefer CLI-manageable tools**: Version-controlled configs > manual dashboards. Infrastructure-as-code > click-ops.

---

## Your Approach

### 1. Detect Current Setup

**Scan for observability tools:**
- Error tracking (Sentry, Bugsnag, Rollbar)
- OpenTelemetry instrumentation
- Analytics (Vercel Analytics, PostHog, Plausible)
- Logging (Pino, Winston, structured logging)
- APM/Tracing (Datadog, New Relic, Elastic APM)
- Monitoring (Grafana, Prometheus)

**Check configurations:**
- Sentry configs (sentry.*.config.ts, instrumentation.ts)
- OpenTelemetry setup (otel.config.ts, telemetry files)
- Analytics integrations (_app.tsx, middleware.ts, layout.tsx)
- GitHub Actions workflows (Sentry releases, deployment notifications)
- CLI automation scripts (observe/alert/monitor scripts)

**Audit environment variables:**
- Sentry: DSN, AUTH_TOKEN, ORG, PROJECT
- OpenTelemetry: EXPORTER endpoints, Grafana Cloud
- Analytics: IDs and public keys
- Logging: LOG_LEVEL, structured logging config
- Check Vercel/Convex env vars if applicable

**Verify deployment integration:**
- Automated Sentry release creation on deploy
- Deployment notifications (GitHub webhooks, Slack)
- Source map uploads for error tracking

### 2. Identify Gaps (Four Pillars)

**Error Tracking:**
- Is Sentry/error tracker installed and configured?
- Are errors being captured across all environments (client, server, edge)?
- Are source maps uploaded for production error debugging?
- Are releases tracked to correlate errors with deployments?
- Is error grouping/deduplication working well?

**Performance Monitoring:**
- Is APM installed (Sentry Performance, OpenTelemetry, Datadog)?
- Are key transactions instrumented (API endpoints, database queries)?
- Is Web Vitals tracking enabled (Core Web Vitals for UX)?
- Are slow queries and N+1 issues detectable?
- Can you trace requests across services?

**Analytics & Product Insights:**
- Is analytics installed (Vercel Analytics, PostHog, Plausible)?
- Are key user actions tracked (sign-ups, conversions, feature usage)?
- Is funnel analysis possible (onboarding, checkout flows)?
- Are A/B tests measurable?
- Is retention/churn trackable?

**Logging & Debugging:**
- Is structured logging enabled (JSON logs with context)?
- Are logs searchable and aggregated (CloudWatch, Datadog, Grafana Loki)?
- Do logs include correlation IDs for request tracing?
- Is sensitive data redacted (PII, secrets)?
- Are log levels configurable per environment?

### 3. Research Modern Patterns (Optional)

**When to research:**
If current setup seems inadequate or you're unfamiliar with modern observability practices.

**Use Gemini CLI for deep research:**
```bash
gemini "Research modern observability patterns for [your stack]:
1. Error tracking best practices (Sentry vs alternatives)
2. OpenTelemetry adoption patterns and benefits
3. Privacy-focused analytics (PostHog, Plausible vs Google Analytics)
4. Structured logging standards (JSON, correlation IDs, log levels)
5. Cost-effective monitoring for [scale/budget]"
```

**When to skip:**
If setup is current and comprehensive.

### 4. Generate Improvement Plan

**Categorize improvements by impact:**

**Critical (Do Immediately):**
- Missing error tracking entirely
- No source maps (can't debug production errors)
- No deployment tracking (can't correlate errors to releases)
- Secrets logged in production

**High Priority (Next Sprint):**
- Missing performance monitoring
- No user analytics (flying blind on product decisions)
- Unstructured logging (difficult debugging)
- Missing key transaction instrumentation

**Medium Priority (Backlog):**
- Advanced tracing (OpenTelemetry adoption)
- Custom dashboards and alerts
- Funnel analysis and A/B testing
- Log aggregation and search

**Low Priority (Nice to Have):**
- Advanced APM features
- Custom metrics and instrumentation
- Real user monitoring enhancements

### 5. Provide CLI Commands

**For each improvement, generate executable CLI commands:**

**Example - Add Sentry to Next.js project:**
```bash
# Install
pnpm add @sentry/nextjs

# Configure (wizard)
npx @sentry/wizard@latest -i nextjs

# Add env vars to Vercel
printf '%s' "$SENTRY_DSN" | vercel env add SENTRY_DSN production
printf '%s' "$SENTRY_AUTH_TOKEN" | vercel env add SENTRY_AUTH_TOKEN production

# Enable source maps in next.config.js
# (Wizard handles this)

# Test
pnpm build
```

**Example - Add structured logging with Pino:**
```bash
# Install
pnpm add pino pino-pretty

# Create logger utility (lib/logger.ts)
# (Provide code template)

# Add to env
echo "LOG_LEVEL=info" >> .env.local

# Test
node -e "require('./lib/logger').info('test')"
```

---

## Observability Stack Recommendations

**Error Tracking:**
- **Sentry** (recommended): Best-in-class error tracking, free tier generous
- Bugsnag: Good alternative, better for mobile
- Rollbar: Simple, effective for smaller teams

**Performance Monitoring:**
- **Sentry Performance** (if using Sentry): Integrated APM, transaction tracing
- OpenTelemetry: Vendor-neutral, future-proof, more complex setup
- Vercel Speed Insights: Built-in for Vercel deployments

**Analytics:**
- **Vercel Analytics** (Vercel projects): Privacy-focused, zero config
- **PostHog** (self-hostable): Product analytics, session replay, feature flags
- Plausible: Privacy-focused, simple, ethical alternative to Google Analytics

**Logging:**
- **Pino** (Node.js): Fastest, structured JSON logging
- Winston: More features, slightly slower
- OpenTelemetry Logs: Unified observability

**Monitoring:**
- Vercel deployment monitoring (built-in)
- Sentry Crons (cron job monitoring)
- Grafana Cloud (open-source, flexible)

---

## Key Principles

**1. Observability as Code**
- All configs in version control
- Infrastructure-as-code (Terraform, Pulumi)
- CLI-driven setup (no manual dashboard clicks)

**2. Privacy-First**
- Redact PII from logs and errors
- Use privacy-focused analytics when possible
- GDPR/CCPA compliance by default

**3. Cost-Effective**
- Leverage free tiers (Sentry, Vercel, PostHog)
- Sample high-volume data appropriately
- Avoid vendor lock-in (prefer OpenTelemetry)

**4. Actionable Alerts**
- Alert on symptoms, not causes
- Reduce alert fatigue (tune thresholds)
- Use Slack/email integrations wisely

**5. Deployment Correlation**
- Track releases in error tracker
- Annotate deployments in monitoring
- Enable automatic rollback triggers

---

## Your Output

**Current State:**
- Tools detected and their configurations
- Environment variable status
- Deployment integration status

**Gap Analysis:**
- Missing pillars (error tracking, performance, analytics, logging)
- Configuration issues
- Integration gaps

**Improvement Plan:**
- Critical/High/Medium/Low priority improvements
- CLI commands for each improvement
- Time/cost estimates
- Recommended tools and rationale

**Quick Wins:**
- 1-2 improvements that provide immediate value with minimal effort
- Executable CLI commands to implement them now

---

## Success Criteria

**Comprehensive observability means:**
- ✓ All production errors captured and debuggable
- ✓ Performance bottlenecks visible and measurable
- ✓ User behavior tracked for product decisions
- ✓ Deployments correlated with error spikes
- ✓ Logs searchable with full context
- ✓ Alerts actionable and low-noise

**If you can answer these questions, you have good observability:**
- What errors happened in the last 24 hours?
- Which API endpoint is slowest?
- How many users completed checkout this week?
- Did the latest deployment cause any new errors?
- Why did this specific request fail?

If you can't answer these: You have observability gaps to fill.
