---
description: Audit and reconcile Stripe subscriptions with database state
---

# /reconcile-subscriptions

> "Trust, but verify."

Run this command to detect drift between Stripe subscription state and your database.

## When to Use

- After billing incidents
- Periodically (weekly audit)
- When customers report subscription issues
- After webhook delivery failures

## Mission

Compare Stripe subscription state with database state to identify:
1. Subscriptions in Stripe but not in database
2. Active subscriptions in database but canceled in Stripe
3. Stale subscription end dates
4. Missing Stripe customer IDs

## Manual Reconciliation Process

### Step 1: Get Stripe Subscriptions

```bash
stripe subscriptions list --status=active --limit=100 --api-key "$STRIPE_SECRET_KEY"
```

Note the customer IDs and subscription statuses.

### Step 2: Query Database

For Convex:
```bash
npx convex run --prod users/queries:getAllSubscribedUsers
```

For other databases, query users where `subscriptionStatus = 'active'`.

### Step 3: Compare

Create two lists:
- **Stripe active:** Customer IDs with active subscriptions in Stripe
- **DB active:** User records with `subscriptionStatus = 'active'`

### Step 4: Identify Drift

| Scenario | Stripe | DB | Action |
|----------|--------|-----|--------|
| Normal | active | active | None |
| Webhook missed | active | null/inactive | Sync from Stripe |
| Cancel missed | canceled | active | Update DB to canceled |
| Customer missing | active | no record | Investigate |

### Step 5: Fix Drift

For missed webhook (active in Stripe, not in DB):
```bash
# Get subscription details
stripe subscriptions retrieve <sub_id> --api-key "$STRIPE_SECRET_KEY"

# Manually sync (project-specific mutation)
npx convex run --prod users/subscriptions:updateSubscription '{
  "stripeCustomerId": "<cus_id>",
  "subscriptionStatus": "active",
  "subscriptionPlan": "monthly",
  "subscriptionEndDate": <timestamp_ms>
}'
```

For canceled subscription not reflected in DB:
```bash
npx convex run --prod users/subscriptions:clearSubscription '{
  "stripeCustomerId": "<cus_id>"
}'
```

## Automated Reconciliation

For projects with a reconciliation cron job, the process is automated:

```typescript
// convex/crons/reconcileSubscriptions.ts
// Runs daily, compares Stripe state with DB, alerts on drift
```

To manually trigger:
```bash
npx convex run --prod crons/reconcileSubscriptions:runReconciliation
```

## Alerting on Drift

Set up alerts for:
- More than 2 subscriptions out of sync
- Any subscription active > 7 days not in DB
- Failed reconciliation runs

## Prevention

To prevent drift in the first place:
1. Use `/billing-preflight` before deployments
2. Monitor `pending_webhooks` metric
3. Ensure webhook URL has no redirects
4. Implement idempotent webhook handling

## Related

- `/billing-preflight` - Pre-deployment checklist
- `/stripe-health` - Webhook diagnostic
- `billing-security` skill - Reference patterns
