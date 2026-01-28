# Stripe API Parameter Constraints

## Checkout Session Mode Constraints

Stripe Checkout has three modes: `payment`, `subscription`, `setup`. Parameters are mode-dependent.

### Mode-Dependent Parameters

| Parameter | payment | subscription | setup |
|-----------|---------|--------------|-------|
| `customer_creation` | valid | INVALID | valid |
| `subscription_data` | INVALID | valid | INVALID |
| `payment_intent_data` | valid | INVALID | INVALID |
| `setup_intent_data` | INVALID | INVALID | valid |

### Common Trap: customer_creation in subscription mode

```typescript
// WRONG - throws error at checkout time
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  customer_creation: "always", // INVALID in subscription mode
  // ...
});

// RIGHT - omit customer_creation in subscription mode
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  // customer is implicitly created for subscriptions
  // ...
});
```

**Error message:** `customer_creation` is only valid in `payment` or `setup` mode.

---

## Webhook Signature Verification

### Required Headers
- `stripe-signature` - HMAC signature of the payload

### Verification Pattern
```typescript
const event = stripe.webhooks.constructEvent(
  body,           // raw request body (string)
  signature,      // stripe-signature header
  webhookSecret   // from STRIPE_WEBHOOK_SECRET env var
);
```

### Common Failures
1. **Body already parsed** - Must use raw body, not JSON-parsed
2. **Wrong secret** - Using test secret in prod or vice versa
3. **Trailing whitespace** - Secret has `\n` at end

---

## API Key Formats

| Key Type | Pattern | Example |
|----------|---------|---------|
| Secret (test) | `sk_test_[a-zA-Z0-9]+` | `sk_test_51ABC...` |
| Secret (live) | `sk_live_[a-zA-Z0-9]+` | `sk_live_51ABC...` |
| Publishable (test) | `pk_test_[a-zA-Z0-9]+` | `pk_test_51ABC...` |
| Publishable (live) | `pk_live_[a-zA-Z0-9]+` | `pk_live_51ABC...` |
| Webhook secret | `whsec_[a-zA-Z0-9]+` | `whsec_abc123...` |

### Validation Regex
```typescript
const STRIPE_SECRET_KEY = /^sk_(test|live)_[a-zA-Z0-9]+$/;
const STRIPE_PUBLISHABLE_KEY = /^pk_(test|live)_[a-zA-Z0-9]+$/;
const STRIPE_WEBHOOK_SECRET = /^whsec_[a-zA-Z0-9]+$/;
```

---

## Webhook URL Requirements

1. **HTTPS required** - HTTP will be rejected
2. **No redirects** - Stripe does NOT follow 3xx responses
3. **Must return 2xx** - 4xx/5xx trigger retries
4. **Timeout: 30 seconds** - Longer processing should be async

### Redirect Trap

```
User configures: https://example.com/webhooks/stripe
Server redirects: 307 → https://www.example.com/webhooks/stripe
Result: Webhook FAILS silently (payload not forwarded through redirect)
```

**Fix:** Always use canonical domain in webhook configuration.

---

## Idempotency

Stripe may deliver the same event multiple times. Handle idempotently:

```typescript
// Track processed events
const processedEvents = new Set<string>();

async function handleWebhook(event: Stripe.Event) {
  if (processedEvents.has(event.id)) {
    return { received: true, duplicate: true };
  }
  processedEvents.add(event.id);
  // ... process event
}
```

Or use database constraint on event ID.

---

## MRR Calculation - Billing Interval Normalization

### Common Mistake
Using `unit_amount` directly for MRR without considering:
1. **Quantity** - subscription items can have quantity > 1
2. **Billing interval** - annual/quarterly subscriptions must be normalized

### Wrong Implementation
```go
// BAD - undercounts MRR for quantity>1, overcounts for annual subscriptions
for _, item := range sub.Items.Data {
    mrr += *item.Price.UnitAmount
}
```

### Correct Implementation
```go
for _, item := range sub.Items.Data {
    qty := int64(1)
    if item.Quantity != nil {
        qty = *item.Quantity
    }
    monthlyRate := *item.Price.UnitAmount * qty

    // Normalize to monthly
    if item.Price.Recurring != nil {
        switch item.Price.Recurring.Interval {
        case "year":
            monthlyRate /= 12
        case "quarter":
            monthlyRate /= 3
        case "week":
            monthlyRate = monthlyRate * 52 / 12
        case "day":
            monthlyRate = monthlyRate * 365 / 12
        }
    }
    mrr += monthlyRate
}
```

### Stripe Price Recurring Object
```json
{
  "recurring": {
    "interval": "year" | "quarter" | "month" | "week" | "day",
    "interval_count": 1
  }
}
```

Note: Also consider `interval_count` for non-standard intervals like "every 2 months".
