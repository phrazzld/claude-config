---
name: stripe-configure
description: |
  Configure Stripe Dashboard and deployment environments.
  Sets up products, prices, webhooks, and environment variables.
effort: high
---

# Stripe Configure

Set up Stripe Dashboard and deployment environment variables.

## Objective

Configure everything outside the codebase: Stripe Dashboard settings, environment variables across all deployments, webhook endpoints.

## Process

**1. Stripe Dashboard Setup**

Guide the user through (or use Stripe CLI where possible):

**Products & Prices**
- Create product (name matches app)
- Create price(s): monthly, annual if applicable
- Note the price IDs for env vars

**Webhook Endpoint**
- Create endpoint pointing to production URL
- Use canonical domain (www if that's where app lives — Stripe doesn't follow redirects)
- Enable required events (from design)
- Copy webhook signing secret

**Customer Portal** (if using)
- Configure allowed actions
- Set branding

**2. Environment Variables**

Set variables on ALL deployment targets. This is where incidents happen.

**IMPORTANT: Stripe test mode is DEPRECATED.**
Two separate Stripe accounts exist:
- **Sandbox** (`acct_...sandbox`): Fully isolated dev account. Use its keys for local dev.
- **Production** (`acct_...prod`): Real money. Only `sk_live_*` keys. Never `sk_test_*`.

**Local Development** (use sandbox account keys)
```bash
# .env.local — keys from SANDBOX account, not production test mode
STRIPE_SECRET_KEY=sk_test_...  # from sandbox account
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...  # from sandbox account
NEXT_PUBLIC_STRIPE_PRICE_ID=price_...
```

**Convex (both dev and prod)**
```bash
# Dev — sandbox account keys
npx convex env set STRIPE_SECRET_KEY "sk_test_..."  # sandbox account
npx convex env set STRIPE_WEBHOOK_SECRET "whsec_..."

# Prod — production account LIVE keys (NEVER sk_test_* from prod account)
npx convex env set --prod STRIPE_SECRET_KEY "sk_live_..."
npx convex env set --prod STRIPE_WEBHOOK_SECRET "whsec_..."
```

**Vercel**
```bash
vercel env add STRIPE_SECRET_KEY production
vercel env add STRIPE_WEBHOOK_SECRET production
# ... etc
```

**3. Verify Parity**

Check that all deployments have matching configuration:
- Local has test keys
- Convex dev has test keys
- Convex prod has live keys
- Vercel prod has live keys

Use `verify-env-parity.sh` if available, or manually compare.

**4. Webhook URL Verification**

CRITICAL: Verify webhook URL doesn't redirect.

```bash
curl -s -o /dev/null -w "%{http_code}" -I -X POST "https://your-domain.com/api/stripe/webhook"
```

Must return 4xx or 5xx, NOT 3xx. If it redirects, fix the URL in Stripe Dashboard.

## Common Mistakes

- Setting env vars on dev but forgetting prod
- Using wrong domain (non-www when app is www)
- Trailing whitespace in secrets (use `printf '%s'` not `echo`)
- **Using sk_test_* from production account** — test mode is DEPRECATED. Use sandbox account for dev, sk_live_* for prod.
- Confusing sandbox account (separate account) with test mode (deprecated feature within production account)

## Output

Checklist of what was configured:
- [ ] Product created
- [ ] Price(s) created
- [ ] Webhook endpoint configured
- [ ] Env vars set on local
- [ ] Env vars set on Convex dev
- [ ] Env vars set on Convex prod
- [ ] Env vars set on Vercel
- [ ] Webhook URL verified (no redirect)
