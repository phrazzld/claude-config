# Common Stripe Integration Pitfalls

Lessons from production incidents and API gotchas.

## Pitfall #1: Dev ≠ Prod Environment Variables

**Symptom:** Integration works locally, fails in production with 500 errors.

**Root Cause:** Env vars set in development but not in production.

**Platforms affected:**
- Convex (separate dev/prod deployments)
- Vercel (separate environment scopes)
- Any platform with environment isolation

**Prevention:**
```bash
# Always verify prod env vars before deploying
CONVEX_DEPLOYMENT=prod:xxx npx convex env list | grep STRIPE
vercel env ls --environment=production | grep STRIPE
```

**Detection:**
- Health endpoint returns Stripe status
- Pre-push hooks verify prod env vars

---

## Pitfall #2: customer_creation in Subscription Mode

**Symptom:** Stripe API error when creating checkout session.

**Root Cause:** `customer_creation` parameter is invalid in `subscription` mode.

**Why it happens:** TypeScript types don't encode mode-dependent constraints.

**The fix:**
```typescript
// ❌ WRONG
stripe.checkout.sessions.create({
  mode: 'subscription',
  customer_creation: 'always', // Invalid!
});

// ✅ CORRECT
stripe.checkout.sessions.create({
  mode: 'subscription',
  // Subscription mode automatically handles customer creation
});
```

**Prevention:** Always verify mode-specific parameters against Stripe docs.

---

## Pitfall #3: Webhook 500s = Config, Not Code

**Symptom:** Webhook endpoint returns 500 in production, works locally.

**Root Cause:** Usually missing `STRIPE_WEBHOOK_SECRET` in production.

**Debug order:**
1. Check env vars first
2. Check Stripe Dashboard webhook logs
3. Then review code

**Not the cause:**
- Code bugs (usually)
- Race conditions (rarely)
- Complex async issues (almost never)

---

## Pitfall #4: Wrong Webhook Secret

**Symptom:** Signature verification fails: "No signatures found matching..."

**Root Cause:** Using dev webhook secret in production (or vice versa).

**Each environment has unique webhook secret:**
- `stripe listen` generates a local secret
- Dashboard webhook generates a different secret
- Test mode and live mode have different secrets

**Prevention:**
```bash
# Verify correct secret for each environment
# Dev: from `stripe listen` output
# Prod: from Stripe Dashboard > Developers > Webhooks > Signing secret
```

---

## Pitfall #5: Trusting TypeScript for API Constraints

**Symptom:** Code compiles but API returns error.

**Root Cause:** Stripe TypeScript types are permissive, not restrictive.

**Examples of uncaught constraints:**
- `customer_creation` only valid in `payment`/`setup` mode
- `trial_period_days` requires `subscription` mode
- Some `payment_method_types` incompatible with certain modes

**Prevention:**
- Always verify against API documentation
- Add unit tests for parameter shapes
- Test with real API in test mode

---

## Pitfall #6: Over-Engineering Under Pressure

**Symptom:** Adding complex code (race condition handling, retry logic) when the real issue is configuration.

**Root Cause:** Debugging code before checking config.

**The pattern:**
1. See 500 error in production
2. Assume code bug
3. Add complex fixes
4. Real issue was missing env var

**Prevention:** Follow "Check Config Before Code" principle:
1. Verify env vars
2. Check Stripe Dashboard
3. Review webhook logs
4. THEN examine code

---

## Pitfall #7: Raw Body Not Preserved

**Symptom:** Webhook signature verification always fails.

**Root Cause:** Middleware parsed JSON before webhook handler.

**The issue:**
```typescript
// Some frameworks auto-parse JSON
app.use(express.json()); // This breaks webhook verification!

// Stripe needs raw body for signature verification
const sig = req.headers['stripe-signature'];
stripe.webhooks.constructEvent(req.rawBody, sig, secret); // Needs raw!
```

**Prevention:**
- Exclude webhook route from body parsing middleware
- Use raw body parser for webhook endpoint
- Next.js App Router: Use `request.text()` not `request.json()`

---

## Pitfall #8: Hardcoded Test Keys in Code

**Symptom:** Test transactions appear in production, or production keys exposed.

**Root Cause:** Keys committed to code instead of env vars.

**Detection:**
```bash
# Scan for hardcoded keys
grep -r "sk_test_\|sk_live_\|pk_test_\|pk_live_" src/ --include="*.ts" --include="*.tsx"
```

**Prevention:**
- Pre-commit hook to scan for key patterns
- Always use `process.env.STRIPE_*`
- Never commit `.env.local`

---

## Pitfall #9: Webhook Endpoint Not Registered

**Symptom:** Events never reach your handler; no webhook logs in Stripe Dashboard.

**Root Cause:** Forgot to register production webhook endpoint.

**Checklist:**
1. Development: `stripe listen --forward-to localhost:3000/api/webhooks`
2. Staging: Dashboard webhook pointing to staging URL
3. Production: Dashboard webhook pointing to production URL

**Each needs its own webhook endpoint registration!**

---

## Pitfall #10: Price IDs Mismatch

**Symptom:** Checkout fails with "No such price" error.

**Root Cause:** Env var contains wrong price ID (test vs live, or old ID).

**Prevention:**
```bash
# Verify price IDs match Stripe Dashboard
stripe prices list --limit 10

# Compare with env vars
echo $NEXT_PUBLIC_STRIPE_MONTHLY_PRICE_ID
echo $NEXT_PUBLIC_STRIPE_ANNUAL_PRICE_ID
```

---

## Debugging Flowchart

```
Production Stripe Error
         │
         ▼
    ┌─────────────┐
    │ Check Env   │──No──► Set missing env vars
    │ Vars Set?   │
    └─────────────┘
         │ Yes
         ▼
    ┌─────────────┐
    │ Check Stripe│──Errors──► Fix API params
    │ Dashboard   │
    └─────────────┘
         │ OK
         ▼
    ┌─────────────┐
    │ Check       │──Failed──► Fix webhook config
    │ Webhooks    │
    └─────────────┘
         │ OK
         ▼
    Now examine code
```
