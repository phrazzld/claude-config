# Environment Variable Format Patterns

Regex patterns for validating common service credentials.

## Stripe

| Variable | Pattern | Example |
|----------|---------|---------|
| `STRIPE_SECRET_KEY` | `^sk_(test\|live)_[A-Za-z0-9]+$` | `sk_live_51xxx` |
| `STRIPE_PUBLISHABLE_KEY` | `^pk_(test\|live)_[A-Za-z0-9]+$` | `pk_live_51xxx` |
| `STRIPE_WEBHOOK_SECRET` | `^whsec_[A-Za-z0-9]+$` | `whsec_xxx` |
| `STRIPE_PRICE_*` | `^price_[A-Za-z0-9]+$` | `price_1xxx` |

## Clerk

| Variable | Pattern | Example |
|----------|---------|---------|
| `CLERK_SECRET_KEY` | `^sk_(test\|live)_[A-Za-z0-9]+$` | `sk_live_xxx` |
| `CLERK_PUBLISHABLE_KEY` | `^pk_(test\|live)_[A-Za-z0-9]+$` | `pk_live_xxx` |
| `CLERK_WEBHOOK_SECRET` | `^whsec_[A-Za-z0-9]+$` | `whsec_xxx` |

## Convex

| Variable | Pattern | Example |
|----------|---------|---------|
| `CONVEX_DEPLOYMENT` | `^(dev\|prod):[a-z-]+(-[0-9]+)?$` | `prod:doting-spider-972` |
| `NEXT_PUBLIC_CONVEX_URL` | `^https://[a-z-]+\.convex\.cloud$` | `https://xxx.convex.cloud` |

## Vercel

| Variable | Pattern | Example |
|----------|---------|---------|
| `BLOB_READ_WRITE_TOKEN` | `^vercel_blob_[A-Za-z0-9_]+$` | `vercel_blob_xxx` |

## Generic Patterns

| Type | Pattern | Notes |
|------|---------|-------|
| Hex token (32 bytes) | `^[a-f0-9]{64}$` | Common for webhook tokens |
| Base64 token | `^[A-Za-z0-9+/]+=*$` | May have padding |
| JWT | `^eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$` | Three base64url parts |

## Validation Script

```bash
validate_format() {
  local var_name=$1
  local value=$2

  case "$var_name" in
    STRIPE_SECRET_KEY)
      [[ "$value" =~ ^sk_(test|live)_[A-Za-z0-9]+$ ]] || return 1
      ;;
    STRIPE_PUBLISHABLE_KEY)
      [[ "$value" =~ ^pk_(test|live)_[A-Za-z0-9]+$ ]] || return 1
      ;;
    STRIPE_WEBHOOK_SECRET)
      [[ "$value" =~ ^whsec_[A-Za-z0-9]+$ ]] || return 1
      ;;
    STRIPE_PRICE_*)
      [[ "$value" =~ ^price_[A-Za-z0-9]+$ ]] || return 1
      ;;
    CLERK_SECRET_KEY)
      [[ "$value" =~ ^sk_(test|live)_[A-Za-z0-9]+$ ]] || return 1
      ;;
    CONVEX_WEBHOOK_TOKEN)
      [[ "$value" =~ ^[a-f0-9]{64}$ ]] || return 1
      ;;
    *)
      return 0  # Unknown format, skip validation
      ;;
  esac
}
```
