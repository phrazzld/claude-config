# Stripe Reconciliation Patterns

## Subscription State Sync

```typescript
// Full subscription reconciliation
export const reconcileAllSubscriptions = internalAction({
  handler: async (ctx) => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
    let hasMore = true
    let startingAfter: string | undefined

    while (hasMore) {
      const subscriptions = await stripe.subscriptions.list({
        limit: 100,
        starting_after: startingAfter,
        expand: ['data.customer'],
      })

      for (const sub of subscriptions.data) {
        const customer = sub.customer as Stripe.Customer

        // Find user by Stripe customer ID
        const user = await ctx.runQuery(internal.users.findByStripeCustomerId, {
          stripeCustomerId: customer.id,
        })

        if (!user) {
          console.warn(`Orphan subscription: ${sub.id} for customer ${customer.id}`)
          continue
        }

        // Compare and update if different
        if (user.subscriptionStatus !== sub.status ||
            user.stripeSubscriptionId !== sub.id) {
          await ctx.runMutation(internal.users.updateSubscription, {
            userId: user._id,
            status: sub.status,
            subscriptionId: sub.id,
            currentPeriodEnd: sub.current_period_end * 1000,
          })
        }
      }

      hasMore = subscriptions.has_more
      if (hasMore) {
        startingAfter = subscriptions.data[subscriptions.data.length - 1].id
      }
    }
  },
})
```

## Event-Based Reconciliation

After discovering missed webhooks:

```typescript
export const replayStripeEvents = internalAction({
  args: {
    sinceHours: v.number(),
    eventTypes: v.optional(v.array(v.string())),
  },
  handler: async (ctx, args) => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
    const since = Math.floor(Date.now() / 1000) - (args.sinceHours * 3600)

    const events = await stripe.events.list({
      created: { gte: since },
      types: args.eventTypes ?? [
        'customer.subscription.created',
        'customer.subscription.updated',
        'customer.subscription.deleted',
        'invoice.paid',
        'invoice.payment_failed',
      ],
      limit: 100,
    })

    const results = {
      processed: 0,
      skipped: 0,
      errors: 0,
    }

    for (const event of events.data) {
      try {
        const existing = await ctx.runQuery(internal.events.exists, {
          eventId: event.id,
        })

        if (existing) {
          results.skipped++
          continue
        }

        await ctx.runAction(internal.webhooks.processEvent, { event })
        results.processed++
      } catch (error) {
        console.error(`Failed to process ${event.id}:`, error)
        results.errors++
      }
    }

    return results
  },
})
```

## Webhook Delivery Check

```typescript
export const checkPendingWebhooks = internalAction({
  handler: async (ctx) => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

    // Get recent events
    const events = await stripe.events.list({
      limit: 20,
      created: { gte: Math.floor(Date.now() / 1000) - 3600 },
    })

    const pending = events.data.filter((e) => e.pending_webhooks > 0)

    if (pending.length > 0) {
      console.warn(`${pending.length} events with pending webhooks`)

      // Return details for investigation
      return pending.map((e) => ({
        id: e.id,
        type: e.type,
        pending: e.pending_webhooks,
        created: new Date(e.created * 1000).toISOString(),
      }))
    }

    return { status: "all_delivered" }
  },
})
```

## Customer Data Sync

```typescript
export const syncCustomerData = internalAction({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const user = await ctx.runQuery(internal.users.get, { id: args.userId })
    if (!user?.stripeCustomerId) return null

    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

    const customer = await stripe.customers.retrieve(user.stripeCustomerId, {
      expand: ['subscriptions', 'invoice_settings.default_payment_method'],
    })

    if (customer.deleted) {
      await ctx.runMutation(internal.users.clearStripeData, { userId: args.userId })
      return { status: "customer_deleted" }
    }

    const subscription = customer.subscriptions?.data[0]
    const paymentMethod = customer.invoice_settings?.default_payment_method as Stripe.PaymentMethod | undefined

    await ctx.runMutation(internal.users.syncStripeData, {
      userId: args.userId,
      email: customer.email,
      subscriptionStatus: subscription?.status ?? null,
      subscriptionId: subscription?.id ?? null,
      currentPeriodEnd: subscription?.current_period_end ? subscription.current_period_end * 1000 : null,
      hasPaymentMethod: !!paymentMethod,
      lastSyncedAt: Date.now(),
    })

    return { status: "synced" }
  },
})
```
