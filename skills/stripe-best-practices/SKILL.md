# Stripe Best Practices

Stripe integration patterns, parameter constraints, and debugging strategies.

## Triggers

Invoke when user mentions:
- "Stripe integration", "payment checkout", "subscription mode"
- "customer_creation parameter", "webhook secret"
- "Stripe test vs live", "Stripe API error"
- Debugging checkout, subscription, or webhook issues

## Core Principles

### 1. TypeScript Types Are Necessary But Not Sufficient

Stripe's TypeScript types don't encode **conditional parameter constraints**:
- `customer_creation` only valid in `payment` or `setup` mode (NOT `subscription`)
- `subscription_data.trial_period_days` requires `subscription` mode
- `payment_intent_data` requires `payment` mode

**Always verify parameter combinations against Stripe API docs, not just TypeScript.**

### 2. Environment Variables: Dev ≠ Prod

For platforms with separate deployments (Convex, Serverless):
- Env vars must be set on **BOTH** dev and prod deployments
- Local `.env.local` doesn't propagate to production
- Use verification scripts before deploying

### 3. Check Config Before Code

When Stripe integrations fail in production:
1. Verify env vars are set (`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`)
2. Check Stripe Dashboard for API errors
3. Review webhook logs for delivery failures
4. **Then** examine code

### 4. Webhook 500s = Usually Config

Production webhook 500 errors typically mean:
- Missing `STRIPE_WEBHOOK_SECRET` in production env
- Wrong webhook endpoint URL registered
- Missing handler for event type

Not usually code bugs.

## Quick Reference

### Required Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `STRIPE_SECRET_KEY` | Backend (Convex/Vercel) | API authentication |
| `STRIPE_WEBHOOK_SECRET` | Backend | Signature verification |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Frontend | Stripe.js initialization |
| `NEXT_PUBLIC_STRIPE_*_PRICE_ID` | Frontend | Checkout price selection |

### Checkout Session Modes

| Mode | Use Case | Special Params |
|------|----------|----------------|
| `payment` | One-time purchase | `payment_intent_data`, `customer_creation` |
| `subscription` | Recurring billing | `subscription_data`, NO `customer_creation` |
| `setup` | Save payment method | `setup_intent_data`, `customer_creation` |

### Webhook Verification Pattern

```typescript
// ALWAYS verify signatures in production
const sig = request.headers.get("stripe-signature");
const event = stripe.webhooks.constructEvent(
  body,
  sig,
  process.env.STRIPE_WEBHOOK_SECRET!
);
```

## Debugging Checklist

When Stripe integration fails:

1. **Environment Check**
   ```bash
   # Convex
   npx convex env list
   CONVEX_DEPLOYMENT=prod:xxx npx convex env list

   # Vercel
   vercel env ls
   ```

2. **Stripe Dashboard**
   - Check Logs > API requests for errors
   - Check Developers > Webhooks for delivery status
   - Verify Products/Prices match env vars

3. **Code Audit**
   - No hardcoded keys (`sk_test_`, `sk_live_`)
   - Correct mode-dependent parameters
   - Webhook signature verification present

## References

See `references/` directory:
- `parameter-constraints.md` - Mode-dependent parameter rules
- `webhook-patterns.md` - Signature verification, idempotency
- `env-var-requirements.md` - Where each variable goes
- `common-pitfalls.md` - Lessons from production incidents

## Audit Script

Run `./scripts/stripe_audit.sh` for automated checks:
```bash
~/.claude/skills/stripe-best-practices/scripts/stripe_audit.sh
```
