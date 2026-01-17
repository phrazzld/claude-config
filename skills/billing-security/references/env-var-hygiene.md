# Environment Variable Hygiene

## The Trailing Whitespace Problem

Environment variables set via CLI or copy-paste often have invisible trailing characters:

```bash
# WRONG - newline gets captured
export STRIPE_WEBHOOK_SECRET="whsec_abc123
"

# Causes: "Invalid character in header content ['\\n']"
```

### Always Trim

```typescript
// WRONG
const secret = process.env.STRIPE_WEBHOOK_SECRET;

// RIGHT
const secret = process.env.STRIPE_WEBHOOK_SECRET?.trim();
```

### Setting Env Vars Safely

```bash
# WRONG - echo adds newline
echo "sk_live_xxx" | vercel env add STRIPE_SECRET_KEY

# RIGHT - printf doesn't add newline
printf '%s' "sk_live_xxx" | vercel env add STRIPE_SECRET_KEY

# RIGHT - bash echo -n (bash-specific)
echo -n "sk_live_xxx" | vercel env add STRIPE_SECRET_KEY
```

---

## Format Validation

Validate format at read time, not request time:

```typescript
// lib/env.ts
function getStripeSecretKey(): string {
  const key = process.env.STRIPE_SECRET_KEY?.trim();

  if (!key) {
    throw new Error("STRIPE_SECRET_KEY not configured");
  }

  if (!/^sk_(test|live)_[a-zA-Z0-9]+$/.test(key)) {
    throw new Error("STRIPE_SECRET_KEY has invalid format");
  }

  return key;
}
```

---

## Cross-Platform Parity

### The Problem

Modern apps often have split deployments:
- **Vercel** - Next.js frontend/API routes
- **Convex** - Backend functions/database

Env vars must be set on BOTH. Easy to forget one.

### The Trap

```bash
# Sets on dev Convex (default)
npx convex env set STRIPE_WEBHOOK_SECRET "whsec_xxx"

# NEVER ran this - prod has no secret
npx convex env set --prod STRIPE_WEBHOOK_SECRET "whsec_xxx"
```

### Verification Script

```bash
#!/bin/bash
# verify-env-parity.sh

REQUIRED_VARS="STRIPE_SECRET_KEY STRIPE_WEBHOOK_SECRET STRIPE_SYNC_SECRET"

echo "Checking Vercel prod..."
VERCEL_VARS=$(vercel env ls --environment=production 2>/dev/null | grep -E "^[A-Z_]+" | cut -d' ' -f1)

echo "Checking Convex prod..."
CONVEX_VARS=$(npx convex env list --prod 2>/dev/null | grep -E "^[A-Z_]+" | cut -d' ' -f1)

MISSING=0
for var in $REQUIRED_VARS; do
  if ! echo "$VERCEL_VARS" | grep -q "^$var$"; then
    echo "MISSING on Vercel: $var"
    MISSING=1
  fi
  if ! echo "$CONVEX_VARS" | grep -q "^$var$"; then
    echo "MISSING on Convex: $var"
    MISSING=1
  fi
done

exit $MISSING
```

---

## Live Mode Detection

Prevent test keys in live environment:

```typescript
function validateKeyMode(key: string, expectedLive: boolean): void {
  const isLive = key.includes("_live_");
  const isTest = key.includes("_test_");

  if (expectedLive && isTest) {
    throw new Error("Test key used in live environment");
  }
  if (!expectedLive && isLive) {
    throw new Error("Live key used in test environment");
  }
}

// Usage
const isLiveEnv = process.env.NODE_ENV === "production";
validateKeyMode(stripeSecretKey, isLiveEnv);
```

---

## Env Var Checklist

Before deploying billing integration:

- [ ] All keys trimmed at read time
- [ ] Format validated with regex
- [ ] Set on Vercel (all environments)
- [ ] Set on Convex (dev AND prod)
- [ ] Live/test mode matches environment
- [ ] No hardcoded keys in code
- [ ] .env files in .gitignore
