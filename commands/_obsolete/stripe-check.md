---
description: Audit Stripe configuration - env vars, webhooks, products, code patterns
---

# Stripe Integration Audit

Audit Stripe configuration for the current project and across the Misty Step account.

## Your Mission

You're a senior SRE auditing Stripe integration. Find configuration issues before they hit production.

## Context

**Current Project Checks:**
- Environment variables across all targets (local, Convex dev/prod, Vercel)
- Code patterns (hardcoded keys, missing webhook verification, mode-dependent params)
- Dashboard alignment via Stripe CLI

**Multi-App Account Checks (Misty Step):**
- Run `~/Development/codex/bin/stripe-audit` to see all apps, webhooks, products, prices
- Naming convention: `{app}__product`, `{app}__interval` (e.g., `chrondle__archive`)
- Webhook domain should match app (chrondle.app → chrondle)

**Known Apps:**
chrondle, volume, bibliomnomnom, caesar, happybirthday, heartbeat, gitpulse, linejam, sploot, timeismoney, scry, vibecheck

## CRITICAL: Webhook URL Verification (Run First!)

**Stripe does NOT follow redirects for POST webhooks.** Always verify before other checks.

```bash
# 1. Get webhook URLs
stripe webhook_endpoints list | grep url

# 2. For EACH URL found, verify no redirects
~/.claude/skills/billing-security/scripts/verify-webhook-url.sh <URL>
```

**Expected:** HTTP 4xx or 5xx (no 3xx redirects)

**If redirect detected:**
- Use canonical domain (typically `www.` prefix)
- Update via: `stripe webhook_endpoints update <id> --url "https://www.<domain>/..."`

This check is MANDATORY. Skip = risk of silent webhook failures.

---

## Key Tools

```bash
# Current project
npx convex env list --prod | grep STRIPE
vercel env ls --environment=production | grep STRIPE

# Multi-app audit
~/Development/codex/bin/stripe-audit --live    # Full audit
~/Development/codex/bin/stripe-audit --check   # Webhook alignment only

# Stripe CLI
stripe webhook_endpoints list
stripe prices list --limit 20
```

## Common Pitfalls

1. **Webhook URL redirects (www vs non-www)** - Stripe won't follow 307/308 redirects. Use canonical domain!
2. **Env vars set on dev but not prod** - Always check both deployments
3. **Trailing `\n` in values** - Causes cryptic "Invalid character" errors
4. **Wrong webhook domain** - Easy to point at wrong app in shared account
5. **Test keys in production** - `sk_test_` should never appear in prod
6. **customer_creation in subscription mode** - Only valid in payment/setup mode

## Subscription/Trial Code Checks

If project has subscription billing, verify these patterns:

### 1. Trial-to-Paid Flow
```bash
# Check if checkout honors remaining trial
grep -r "trial_end" --include="*.ts" app/ lib/
```
**Expected:** Checkout passes `trial_end` to `subscription_data` when user has remaining trial.

### 2. Zombie Trial Prevention
```bash
# Check if trial is cleared when subscription activates
grep -r "trialEndsAt.*0\|trialEndsAt: 0" --include="*.ts" convex/
```
**Expected:** Webhook handler sets `trialEndsAt = 0` when `subscriptionStatus` becomes `active`.

### 3. Access Control Priority
```bash
# Check hasAccess function order
grep -A 30 "hasAccess" --include="*.ts" convex/ lib/
```
**Expected order:**
1. Active subscription → grant
2. Canceled in paid period → grant
3. Past due in grace period → grant
4. Locked states (incomplete, unpaid, expired) → **deny before trial check**
5. Trial active → grant
6. Default → deny

**Red flag:** Checking trial before locked states allows zombie trial access.

### 4. Idempotency
```bash
# Check webhook deduplication
grep -r "eventId\|lastStripeEvent" --include="*.ts" convex/
```
**Expected:** Webhook handler rejects duplicate `eventId` and stale `eventTimestamp`.

## Report Format

Produce a concise status table, list issues found, and recommend fixes.

## Philosophy

> "Check config before code."

Most Stripe "bugs" are configuration issues. Verify env vars and dashboard state before reading code.
