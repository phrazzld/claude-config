---
description: Compare env vars across platforms (Vercel, Convex, local) for mismatches
---

# ENV-PARITY-CHECK

> **THE SILENT KILLER**
>
> **Postmortem Lesson**: "Webhooks silently fail when CONVEX_WEBHOOK_TOKEN is set on Vercel but not Convex."
>
> **Root Cause**: Separate deployment platforms = separate env var stores = easy to miss one.

**Cross-platform env var verification.** When Vercel and Convex need the same secret (like `CONVEX_WEBHOOK_TOKEN`), a mismatch causes silent failures with no errors in logs.

## Your Mission

Compare environment variables across deployment platforms (Vercel ↔ Convex ↔ Local) and identify:
1. Variables missing from one platform
2. Variables with mismatched values
3. Variables with format issues (trailing whitespace, wrong prefix)

## Execution Flow

### Phase 1: Gather Environment State

**Local (.env.local):**
```bash
# List all local env vars (sanitized - no values)
grep -E "^[A-Z_]+=" .env.local 2>/dev/null | cut -d= -f1 | sort
```

**Convex Production:**
```bash
# Use --prod flag (NOT env var)
npx convex env list --prod | cut -d= -f1 | sort
```

**Vercel Production:**
```bash
# List production env vars
vercel env ls --environment=production 2>/dev/null | grep -E "^[A-Z_]+" | awk '{print $1}' | sort
```

### Phase 2: Identify Shared Variables

These variables MUST exist on both Vercel and Convex:

| Variable | Purpose | Must Match |
|----------|---------|------------|
| `CONVEX_WEBHOOK_TOKEN` | Webhook authentication | Yes |
| `STRIPE_SECRET_KEY` | Stripe API | Backend only (Convex) |
| `STRIPE_WEBHOOK_SECRET` | Webhook verification | Backend only (Convex) |

### Phase 3: Check Parity

**CONVEX_WEBHOOK_TOKEN (Critical):**
```bash
echo "=== CONVEX_WEBHOOK_TOKEN Parity Check ==="

# Convex
echo "Convex prod:"
npx convex env list --prod 2>/dev/null | grep "^CONVEX_WEBHOOK_TOKEN=" && echo "  EXISTS" || echo "  MISSING!"

# Vercel
echo "Vercel prod:"
vercel env ls --environment=production 2>/dev/null | grep "CONVEX_WEBHOOK_TOKEN" && echo "  EXISTS (value hidden)" || echo "  MISSING!"

# If both exist, remind user to verify values match
echo ""
echo "NOTE: Vercel hides values. Verify manually in Vercel Dashboard if both exist."
```

**Format Validation (Convex):**
```bash
echo "=== Format Validation ==="

npx convex env list --prod | while IFS= read -r line; do
  var_name=$(echo "$line" | cut -d= -f1)
  value=$(echo "$line" | cut -d= -f2-)

  # Check for trailing whitespace
  if [[ "$value" =~ [[:space:]]$ ]] || [[ "$value" == *'\n'* ]]; then
    echo "WARNING: $var_name has trailing whitespace"
  fi

  # Check format for known patterns
  case "$var_name" in
    STRIPE_SECRET_KEY)
      [[ "$value" =~ ^sk_(test|live)_[A-Za-z0-9]+$ ]] || echo "ERROR: $var_name invalid format"
      ;;
    STRIPE_WEBHOOK_SECRET)
      [[ "$value" =~ ^whsec_[A-Za-z0-9]+$ ]] || echo "ERROR: $var_name invalid format"
      ;;
  esac
done
```

### Phase 4: Generate Report

```markdown
## Environment Parity Report

**Date**: [timestamp]
**Project**: [name]

---

### Platform Comparison

| Variable | Local | Convex (prod) | Vercel (prod) | Status |
|----------|-------|---------------|---------------|--------|
| CONVEX_WEBHOOK_TOKEN | ✅/❌ | ✅/❌ | ✅/❌ | ✅ Parity / ⚠️ Mismatch |
| STRIPE_SECRET_KEY | ✅/❌ | ✅/❌ | N/A | ✅ OK |
| ... | | | | |

---

### Issues Found

1. **[CRITICAL/WARNING]**: [Description]
   - **Impact**: [What fails]
   - **Fix**: [Command to run]

---

### Recommendations

1. Set missing variables
2. Fix format issues
3. Verify parity in Vercel Dashboard

---

**Overall Status**: ✅ PARITY / ⚠️ MISMATCH / ❌ MISSING
```

## Quick Commands

```bash
# Check if CONVEX_WEBHOOK_TOKEN exists on Convex
npx convex env list --prod | grep CONVEX_WEBHOOK_TOKEN

# Check if CONVEX_WEBHOOK_TOKEN exists on Vercel
vercel env ls --environment=production | grep CONVEX_WEBHOOK_TOKEN

# Set token on Convex (if missing) - use printf to avoid trailing newline
npx convex env set --prod CONVEX_WEBHOOK_TOKEN "$(printf '%s' 'your-token-here')"

# Set token on Vercel (if missing)
printf '%s' 'your-token-here' | vercel env add CONVEX_WEBHOOK_TOKEN production
```

## Common Issues

### Token on Vercel but not Convex

**Symptom**: Webhooks reach Vercel, but Convex action rejects them.

**Fix**:
```bash
# Get token from Vercel Dashboard, then set on Convex
npx convex env set --prod CONVEX_WEBHOOK_TOKEN "$(printf '%s' 'token-from-vercel')"
```

### Token on Convex but not Vercel

**Symptom**: Webhook handler can't verify incoming requests.

**Fix**:
```bash
# Get token from Convex, then set on Vercel
printf '%s' 'token-from-convex' | vercel env add CONVEX_WEBHOOK_TOKEN production
```

### Values Don't Match

**Symptom**: Signature verification fails intermittently.

**Fix**: Pick one source of truth (generate new token), set on both:
```bash
# Generate new token
NEW_TOKEN=$(openssl rand -hex 32)

# Set on both platforms
npx convex env set --prod CONVEX_WEBHOOK_TOKEN "$(printf '%s' "$NEW_TOKEN")"
printf '%s' "$NEW_TOKEN" | vercel env add CONVEX_WEBHOOK_TOKEN production

# Redeploy Vercel to pick up new env var
vercel --prod
```

## Philosophy

> **"Silent failures are the worst failures."**

When webhooks fail silently because of env var mismatches:
- No error logs to investigate
- No alerts to trigger
- Data just... doesn't sync

This command exists to make the invisible visible. Run it before every production deployment.

---

*Based on 2026-01-17 incident: 45 minutes wasted debugging "code bugs" that were actually configuration mismatches.*
