# Reconciliation Monitoring

## Drift Detection Metrics

Track these metrics to detect sync issues:

### Subscription Drift Rate
```typescript
export const measureDrift = internalQuery({
  handler: async (ctx) => {
    const users = await ctx.db
      .query("users")
      .filter((q) => q.neq(q.field("stripeCustomerId"), null))
      .collect()

    const stale = users.filter((u) => {
      // Not synced in last 24 hours
      return !u.lastSyncedAt || Date.now() - u.lastSyncedAt > 86400000
    })

    const mismatch = users.filter((u) => {
      // Has subscription but missing Stripe ID (or vice versa)
      return (u.subscriptionStatus === 'active' && !u.stripeSubscriptionId) ||
             (u.subscriptionStatus !== 'active' && u.stripeSubscriptionId)
    })

    return {
      total: users.length,
      stale: stale.length,
      stalePercent: (stale.length / users.length * 100).toFixed(2),
      mismatch: mismatch.length,
      mismatchPercent: (mismatch.length / users.length * 100).toFixed(2),
    }
  },
})
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Stale users (>24h) | >5% | >10% |
| Status mismatch | >1% | >5% |
| Pending webhooks | >5 | >20 |
| Failed reconciliations | >1 | >5 |

## Logging Strategy

### Reconciliation Runs

```typescript
// Log at start
console.log('Reconciliation started', {
  type: 'subscriptions',
  scope: 'all',
  timestamp: new Date().toISOString(),
})

// Log each fix
console.log('Drift corrected', {
  userId: user._id,
  field: 'subscriptionStatus',
  was: user.subscriptionStatus,
  now: stripeStatus,
  source: 'stripe_api',
})

// Log completion
console.log('Reconciliation completed', {
  type: 'subscriptions',
  duration: Date.now() - startTime,
  checked: totalChecked,
  fixed: totalFixed,
  errors: totalErrors,
})
```

### Structured Logging

```typescript
const reconciliationLog = {
  event: 'reconciliation',
  service: 'stripe',
  entity: 'subscription',
  userId: user._id,
  drift: {
    field: 'status',
    local: user.subscriptionStatus,
    remote: stripeStatus,
  },
  action: 'updated',
  timestamp: new Date().toISOString(),
}
console.log(JSON.stringify(reconciliationLog))
```

## Alerting

### Slack/Discord Webhook

```typescript
async function alertDrift(drift: DriftReport) {
  if (drift.mismatchPercent > 5) {
    await fetch(process.env.SLACK_WEBHOOK_URL!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: `High drift detected: ${drift.mismatchPercent}% subscription mismatches`,
        blocks: [
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: `*Subscription Drift Alert*\n• Mismatched: ${drift.mismatch}/${drift.total}\n• Stale: ${drift.stale}\n• Check Stripe dashboard and run reconciliation`,
            },
          },
        ],
      }),
    })
  }
}
```

## Dashboard Queries

### Recent Reconciliation History

```typescript
export const getReconciliationHistory = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("reconciliationRuns")
      .order("desc")
      .take(args.limit ?? 10)
  },
})
```

### User Sync Status

```typescript
export const getUserSyncStatus = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId)
    if (!user) return null

    return {
      lastSyncedAt: user.lastSyncedAt,
      timeSinceSync: user.lastSyncedAt
        ? Math.floor((Date.now() - user.lastSyncedAt) / 60000) + ' minutes'
        : 'never',
      subscriptionStatus: user.subscriptionStatus,
      hasStripeData: !!user.stripeCustomerId,
    }
  },
})
```
