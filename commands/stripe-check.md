# STRIPE-CHECK

> **THE INTEGRATION MASTERS**
>
> **Stripe Postmortem Lesson**: "TypeScript types don't encode Stripe's conditional parameter constraints."
>
> **Production Wisdom**: "Check config before code when debugging external services."
>
> **Deployment Truth**: "Dev ≠ Prod is a footgun. Env vars must be set on BOTH deployments."

**External APIs fail differently than local code.** Configuration issues masquerade as code bugs. This command audits your Stripe integration to catch common pitfalls before they hit production.

## Your Mission

Systematically audit the Stripe integration in the current project, checking:
1. Environment variables across all deployment targets
2. Code patterns for common mistakes
3. Webhook security and configuration
4. Stripe Dashboard alignment (via CLI if available)

## Execution Flow

### Phase 1: Detection

First, detect the project type and Stripe usage:

```bash
# Detect if Stripe SDK is installed
grep '"stripe"' package.json

# Find Stripe-related files
rg -l "stripe" --type ts --type tsx src/ convex/
```

Report findings:
- Project type (Convex, Vercel, generic Node.js)
- Stripe SDK version
- Locations of Stripe code

### Phase 2: Environment Audit

Check environment variables across all targets.

**Local Environment:**
```bash
# Check .env.local
grep "STRIPE" .env.local 2>/dev/null || echo "No .env.local found"
```

**Convex (if applicable):**
```bash
# Dev environment
npx convex env list | grep STRIPE

# Production environment
CONVEX_DEPLOYMENT=prod:xxx npx convex env list | grep STRIPE
```

**Vercel (if applicable):**
```bash
vercel env ls | grep STRIPE
```

**Required Variables:**
| Variable | Required In | Purpose |
|----------|-------------|---------|
| `STRIPE_SECRET_KEY` | Backend | API authentication |
| `STRIPE_WEBHOOK_SECRET` | Backend | Signature verification |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Frontend | Stripe.js init |
| `NEXT_PUBLIC_STRIPE_*_PRICE_ID` | Frontend | Price selection |

### Phase 3: Code Audit

Scan for common mistakes:

**Hardcoded Keys:**
```bash
# Should return empty
rg "sk_test_|sk_live_|pk_test_|pk_live_|whsec_" --type ts --type tsx src/
```

**Mode-Dependent Parameters:**
```bash
# Check for customer_creation in subscription mode
rg "mode.*subscription" -A5 --type ts | rg "customer_creation"
```

**Webhook Security:**
```bash
# Verify signature verification exists
rg "stripe.webhooks.constructEvent|constructEvent" --type ts
```

### Phase 4: Dashboard Verification (Stripe CLI)

If Stripe CLI is available and authenticated:

```bash
# Check webhook endpoints
stripe webhook_endpoints list --limit 5

# Verify price IDs exist
stripe prices retrieve $NEXT_PUBLIC_STRIPE_MONTHLY_PRICE_ID
stripe prices retrieve $NEXT_PUBLIC_STRIPE_ANNUAL_PRICE_ID

# Check recent events for errors
stripe events list --limit 10
```

### Phase 5: Report

Generate a comprehensive report:

```markdown
## Stripe Integration Audit Report

**Project**: [name]
**Date**: [timestamp]
**Project Type**: [convex/vercel/node]

---

### Environment Variables

| Target | Status | Missing |
|--------|--------|---------|
| Local (.env.local) | ✅ / ⚠️ / ❌ | [list] |
| Convex (dev) | ✅ / ⚠️ / ❌ | [list] |
| Convex (prod) | ✅ / ⚠️ / ❌ | [list] |
| Vercel | ✅ / ⚠️ / ❌ | [list] |

---

### Code Quality

| Check | Status | Details |
|-------|--------|---------|
| No hardcoded keys | ✅ / ❌ | [locations if any] |
| Webhook verification | ✅ / ❌ | [file location] |
| Mode-dependent params | ✅ / ⚠️ | [potential issues] |
| Health endpoint | ✅ / ⚠️ | [includes Stripe?] |

---

### Dashboard Alignment (Stripe CLI)

| Check | Status | Details |
|-------|--------|---------|
| Webhook endpoints | ✅ / ⚠️ | [count registered] |
| Price IDs valid | ✅ / ❌ | [verified in Stripe] |
| Test/Live alignment | ✅ / ⚠️ | [mode consistency] |

---

### Issues Found

1. **[CRITICAL/WARNING]**: [Issue description]
   - **Impact**: [What could go wrong]
   - **Fix**: [How to resolve]
   - **Reference**: [Link to skill docs]

---

### Recommendations

1. [Priority action]
2. [Next action]
3. [Future improvement]

---

**Overall Status**: ✅ PASS / ⚠️ WARNINGS / ❌ FAIL
```

## Automated Script

For quick checks, run the audit script:

```bash
~/.claude/skills/stripe-best-practices/scripts/stripe_audit.sh
```

Options:
- `--local-only`: Skip Stripe CLI checks
- `--quiet`: Minimal output (pass/fail only)

## Common Issues and Fixes

### Missing Prod Env Vars

**Symptom**: Works in dev, 500 errors in production.

**Fix**:
```bash
CONVEX_DEPLOYMENT=prod:xxx npx convex env set STRIPE_SECRET_KEY "sk_live_..."
CONVEX_DEPLOYMENT=prod:xxx npx convex env set STRIPE_WEBHOOK_SECRET "whsec_..."
```

### customer_creation in Subscription Mode

**Symptom**: Stripe API error on checkout.

**Fix**: Remove `customer_creation` parameter when mode is `subscription`.

See: `~/.claude/skills/stripe-best-practices/references/parameter-constraints.md`

### Webhook Signature Verification Missing

**Symptom**: Webhooks work but are insecure.

**Fix**: Add `stripe.webhooks.constructEvent()` with signature verification.

See: `~/.claude/skills/stripe-best-practices/references/webhook-patterns.md`

### Hardcoded Keys in Code

**Symptom**: Keys exposed in version control.

**Fix**: Move to environment variables, add to .gitignore.

## Skill Integration

This command uses the `stripe-best-practices` skill for remediation guidance:

```
~/.claude/skills/stripe-best-practices/
├── SKILL.md                    # Core patterns and principles
└── references/
    ├── parameter-constraints.md    # Mode-dependent params
    ├── webhook-patterns.md         # Webhook best practices
    ├── env-var-requirements.md     # Where vars go
    └── common-pitfalls.md          # Lessons learned
```

## Philosophy

> **"Check config before code."**

When external integrations fail:
1. Verify environment variables first
2. Check the external service's dashboard
3. Review webhook delivery logs
4. THEN examine your code

Most "code bugs" in external integrations are actually configuration issues.

---

*This command codifies lessons from production incidents. The few minutes spent auditing saves hours of debugging.*
