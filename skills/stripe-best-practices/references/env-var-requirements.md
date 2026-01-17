# Stripe Environment Variable Requirements

Where each Stripe environment variable should be configured.

## Variable Reference

| Variable | Frontend | Backend | Purpose |
|----------|----------|---------|---------|
| `STRIPE_SECRET_KEY` | ❌ Never | ✅ Required | API authentication |
| `STRIPE_WEBHOOK_SECRET` | ❌ Never | ✅ Required | Webhook signature verification |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | ✅ Required | Optional | Stripe.js client initialization |
| `NEXT_PUBLIC_STRIPE_MONTHLY_PRICE_ID` | ✅ Required | Optional | Price selection in UI |
| `NEXT_PUBLIC_STRIPE_ANNUAL_PRICE_ID` | ✅ Required | Optional | Price selection in UI |

## Platform-Specific Configuration

### Next.js + Vercel

```bash
# .env.local (development)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_STRIPE_MONTHLY_PRICE_ID=price_...
NEXT_PUBLIC_STRIPE_ANNUAL_PRICE_ID=price_...

# Vercel (production)
vercel env add STRIPE_SECRET_KEY production
vercel env add STRIPE_WEBHOOK_SECRET production
vercel env add NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY production
vercel env add NEXT_PUBLIC_STRIPE_MONTHLY_PRICE_ID production
vercel env add NEXT_PUBLIC_STRIPE_ANNUAL_PRICE_ID production
```

### Convex Backend

Convex has **separate dev and prod deployments**. Env vars must be set on BOTH.

```bash
# Development
npx convex env set STRIPE_SECRET_KEY "sk_test_..."
npx convex env set STRIPE_WEBHOOK_SECRET "whsec_..."

# Production (CRITICAL - often forgotten!)
CONVEX_DEPLOYMENT=prod:xxx npx convex env set STRIPE_SECRET_KEY "sk_live_..."
CONVEX_DEPLOYMENT=prod:xxx npx convex env set STRIPE_WEBHOOK_SECRET "whsec_..."
```

**Common mistake:** Setting env vars in dev and assuming they propagate to prod.

### Next.js + Convex Hybrid

When using Next.js API routes AND Convex:

| Variable | Next.js (.env) | Convex (env set) |
|----------|----------------|------------------|
| `STRIPE_SECRET_KEY` | If API routes | If HTTP actions |
| `STRIPE_WEBHOOK_SECRET` | If Next.js webhook | If Convex webhook |
| `NEXT_PUBLIC_*` | ✅ Yes | Not needed |

## Verification Commands

### Convex

```bash
# List dev env vars
npx convex env list

# List prod env vars
CONVEX_DEPLOYMENT=prod:xxx npx convex env list

# Check specific var exists
npx convex env list | grep STRIPE_SECRET_KEY
```

### Vercel

```bash
# List all env vars
vercel env ls

# List production only
vercel env ls --environment=production
```

### Local (.env files)

```bash
# Check .env.local exists and has Stripe vars
grep STRIPE .env.local

# Ensure no secrets in .env (committed file)
grep -r "sk_test_\|sk_live_" .env
```

## Test vs Live Keys

### Key Prefixes

| Prefix | Environment | Use Case |
|--------|-------------|----------|
| `pk_test_` | Test | Development, staging |
| `sk_test_` | Test | Development, staging |
| `pk_live_` | Live | Production |
| `sk_live_` | Live | Production |
| `whsec_` | Both | Webhook secrets (test or live) |

### Environment Alignment

Ensure consistent test/live across all vars:

```bash
# ✅ CORRECT - All test keys
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# ❌ WRONG - Mixed test/live
STRIPE_SECRET_KEY=sk_live_...          # Live
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...  # Test!
```

## Pre-Deployment Checklist

Before deploying to production:

1. **Verify prod env vars exist:**
   ```bash
   CONVEX_DEPLOYMENT=prod:xxx npx convex env list | grep STRIPE
   vercel env ls --environment=production | grep STRIPE
   ```

2. **Verify using live keys:**
   ```bash
   # Should see sk_live_ and pk_live_ prefixes
   ```

3. **Verify webhook endpoint registered:**
   - Stripe Dashboard > Developers > Webhooks
   - Production URL matches deployment

4. **Test with real API:**
   - Use Stripe test mode for staging
   - Verify events appear in Dashboard

## Security Rules

### Never Commit Secrets

```gitignore
# .gitignore
.env.local
.env*.local
```

### Never Expose in Frontend

```typescript
// ❌ WRONG - Secret key in client code
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY); // In React component

// ✅ CORRECT - Only publishable key in frontend
import { loadStripe } from '@stripe/stripe-js';
const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);
```

### Scan for Hardcoded Keys

```bash
# Find any hardcoded Stripe keys
grep -r "sk_test_\|sk_live_\|pk_test_\|pk_live_" src/
```
