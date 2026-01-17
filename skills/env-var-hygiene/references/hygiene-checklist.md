# Environment Variable Hygiene Checklist

Run through this checklist before every production deployment.

## Pre-Deployment Checklist

### 1. Presence Check

All required variables exist on production:

- [ ] Convex prod: `npx convex env list --prod`
- [ ] Vercel prod: `vercel env ls --environment=production`

### 2. Format Validation

Variables match expected patterns:

- [ ] `STRIPE_SECRET_KEY` starts with `sk_live_` (production) or `sk_test_` (dev)
- [ ] `STRIPE_WEBHOOK_SECRET` starts with `whsec_`
- [ ] `STRIPE_PRICE_*` starts with `price_`
- [ ] `CONVEX_WEBHOOK_TOKEN` is 64 hex characters

### 3. Whitespace Check

No trailing whitespace or newlines:

```bash
npx convex env list --prod | while IFS= read -r line; do
  var=$(echo "$line" | cut -d= -f1)
  val=$(echo "$line" | cut -d= -f2-)
  if [[ "$val" =~ [[:space:]]$ ]] || [[ "$val" == *'\n'* ]]; then
    echo "ERROR: $var has whitespace issues"
  fi
done
```

### 4. Cross-Platform Parity

Shared tokens are identical on both platforms:

- [ ] `CONVEX_WEBHOOK_TOKEN` exists on Convex AND Vercel
- [ ] Values match (verify in Vercel Dashboard)

### 5. Environment Consistency

Production uses production keys:

- [ ] `STRIPE_SECRET_KEY` uses `sk_live_` not `sk_test_`
- [ ] `CLERK_SECRET_KEY` uses `sk_live_` not `sk_test_`
- [ ] No test/sandbox URLs in production vars

## Quick Verification Commands

```bash
# All-in-one check
./scripts/validate-env.sh --prod-only

# Or manual:
npx convex env list --prod | head -20
vercel env ls --environment=production | head -20
```

## Common Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Trailing `\n` | "Invalid character in header" | Re-set with `printf` |
| Token mismatch | Silent webhook failures | Regenerate and set both |
| Test key in prod | Live charges fail | Update to live key |
| Missing var | 500 errors | Set the missing var |
