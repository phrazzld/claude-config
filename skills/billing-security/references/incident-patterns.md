# Incident Patterns: 3 Stripe Failures in 24 Hours

## Overview

Three projects (chrondle, bibliomnomnom, volume) shipped Stripe integrations in 24 hours. **All 3 had prod failures.** All passed code review. Root causes were configuration, not code.

---

## Incident 1: Chrondle (2026-01-17)

### Symptom
Customer completed checkout, subscription not activated. No errors in logs.

### Root Cause
Webhook URL `https://chrondle.app/api/webhooks/stripe` returned **307 redirect** to `https://www.chrondle.app/...`

**Stripe does NOT follow redirects for POST requests.** Webhook silently failed.

### Evidence
```bash
$ curl -I -X POST https://chrondle.app/api/webhooks/stripe
HTTP/2 307
location: https://www.chrondle.app/api/webhooks/stripe
```

### Fix
Updated Stripe webhook endpoint to canonical URL: `https://www.chrondle.app/api/webhooks/stripe`

### Lesson
**Always use canonical domain.** Check for redirects with `curl -I` before configuring webhook.

---

## Incident 2: Bibliomnomnom (2026-01-17)

### Symptom
Checkout succeeded, subscription state never synced. Customer saw "14 days left in trial" despite payment.

### Root Cause
`CONVEX_WEBHOOK_TOKEN` had **trailing newline** from copy-paste.

Error: `Invalid character in header content ['\n']`

### Evidence
Webhook signature verification failed. Spent 45 minutes debugging wrong environment before finding the newline.

### Fix
```bash
# Re-set without newline
printf '%s' "correct_token" | npx convex env set --prod CONVEX_WEBHOOK_TOKEN
```

### Lesson
**Always trim env vars.** Use `printf '%s'` not `echo` when setting via CLI.

---

## Incident 3: Volume (2026-01-16)

### Symptom
1. Checkout rejected: "customer_creation invalid in subscription mode"
2. After fix, webhooks returning 500 silently

### Root Cause (Part 1)
Used `customer_creation: "always"` in subscription mode. Invalid parameter combination.

### Root Cause (Part 2)
Env vars set on **dev Convex only**. Never ran with `--prod` flag.

```bash
# What was run (dev only)
npx convex env set STRIPE_WEBHOOK_SECRET "whsec_xxx"

# What was needed (prod)
npx convex env set --prod STRIPE_WEBHOOK_SECRET "whsec_xxx"
```

### Evidence
Webhooks returned 500 because `process.env.STRIPE_WEBHOOK_SECRET` was undefined in prod.

### Lesson
1. **Know Stripe parameter constraints** - mode-dependent params
2. **Always use --prod flag** - or verify with `npx convex env list --prod`

---

## Common Threads

| Pattern | Chrondle | Bibliomnomnom | Volume |
|---------|----------|---------------|--------|
| Passed code review | Yes | Yes | Yes |
| Config issue, not code | Yes | Yes | Yes |
| Silent failure | Yes | Yes | Yes |
| No logs = no request | Yes | - | Yes |
| Env var problem | - | Yes | Yes |

---

## Anti-Pattern: "The Code Looks Right"

All 3 incidents had this debugging pattern:
1. Check code → looks correct
2. Check dashboard → looks configured
3. Check env vars → appear to be set
4. Conclude "it should work"

**Problem:** Checked configuration (intent), not runtime behavior (reality).

**Fix:** Always verify with observables:
- `curl -I` to test actual HTTP response
- `stripe events list` to check `pending_webhooks`
- Tail logs during test event resend

---

## Prevention Checklist

Before any billing deploy:

- [ ] `curl -I -X POST <webhook_url>` returns non-3xx
- [ ] `npx convex env list --prod | grep STRIPE` shows all required vars
- [ ] `vercel env ls production | grep STRIPE` shows all required vars
- [ ] No `customer_creation` in subscription mode
- [ ] All env vars read with `.trim()`
- [ ] Test with real Stripe test event (not just unit tests)
