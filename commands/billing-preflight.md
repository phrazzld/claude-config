---
description: Pre-deployment checklist for billing integrations
---

# /billing-preflight

> "Configuration is not reality. Verification must be active, not passive."

Run this command before deploying any billing integration changes.

## Mission

Verify that all billing/payment configuration is correct before deployment:
1. Webhook URL reachability (no redirects)
2. Environment variable parity (Vercel + Convex)
3. Stripe configuration health
4. Code patterns compliance

## Checklist

### 1. Webhook URL Verification

Run the webhook URL check:

```bash
~/.claude/skills/billing-security/scripts/verify-webhook-url.sh <WEBHOOK_URL>
```

**Must pass:** URL returns non-3xx status (Stripe doesn't follow redirects).

### 2. Environment Parity

Run the env parity check:

```bash
~/.claude/skills/billing-security/scripts/verify-env-parity.sh
```

**Must pass:** Required billing env vars exist on both Vercel and Convex prod.

### 3. Stripe Configuration Audit

Run the full Stripe audit:

```bash
python3 ~/.claude/skills/billing-security/scripts/audit-stripe-config.py --domain <YOUR_DOMAIN>
```

**Check for:**
- Single endpoint per domain (no duplicates)
- All endpoints enabled
- Recent events delivered (low pending_webhooks)

### 4. Code Patterns

Verify code follows billing security patterns:

- [ ] All env vars read with `.trim()`
- [ ] API key formats validated
- [ ] Webhook handler returns 200 on all paths (prevent Stripe retries)
- [ ] No hardcoded API keys in code
- [ ] Signature verification enabled

### 5. Manual Verification

After automated checks pass:

- [ ] Test checkout flow in Stripe test mode
- [ ] Verify webhook receives test event (check logs)
- [ ] Confirm database state updates correctly

## Go/No-Go Decision

```
ALL automated checks pass? [Y/N]
Manual verification complete? [Y/N]
Env vars set on BOTH Vercel AND Convex prod? [Y/N]

If all Y: PROCEED with deployment
If any N: FIX issues first
```

## Post-Deployment

After deployment:

1. Monitor first real webhook delivery
2. Check `pending_webhooks` metric
3. Verify customer subscription state syncs

## Related

- `/stripe-health` - Quick webhook diagnostic
- `/reconcile-subscriptions` - Stripe/DB sync audit
- `billing-security` skill - Reference patterns
