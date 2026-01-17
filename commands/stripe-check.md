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

1. **Env vars set on dev but not prod** - Always check both deployments
2. **Trailing `\n` in values** - Causes cryptic "Invalid character" errors
3. **Wrong webhook domain** - Easy to point at wrong app in shared account
4. **Test keys in production** - `sk_test_` should never appear in prod
5. **customer_creation in subscription mode** - Only valid in payment/setup mode

## Report Format

Produce a concise status table, list issues found, and recommend fixes.

## Philosophy

> "Check config before code."

Most Stripe "bugs" are configuration issues. Verify env vars and dashboard state before reading code.
