---
description: Comprehensive pre-deployment checklist for env vars, tests, git status
---

# PRE-DEPLOY

> **THE FRIDAY AFTERNOON TEST**
>
> **Quality Gates Principle**: "If you can't merge on Friday afternoon and turn off your phone, your quality gates are insufficient."
>
> **Postmortem Wisdom**: "Configuration errors are invisible until they cause production failures."

**Universal pre-deployment checklist.** Before deploying to production, verify everything is ready. This command adapts to your project type (Convex, Vercel, generic).

## Your Mission

Run a comprehensive pre-deployment verification:
1. Detect project type and deployment targets
2. Validate environment variables (presence, format, parity)
3. Check git status and branch
4. Run tests and type checks
5. Generate go/no-go report

## Execution Flow

### Phase 1: Project Detection

Detect what kind of project this is:

```bash
# Check for Convex
[[ -f convex.json ]] && echo "Convex project detected"

# Check for Vercel
[[ -f vercel.json ]] && echo "Vercel project detected"

# Check for Next.js
[[ -f next.config.ts ]] || [[ -f next.config.js ]] && echo "Next.js project detected"

# Check package manager
[[ -f pnpm-lock.yaml ]] && PM="pnpm"
[[ -f yarn.lock ]] && PM="yarn"
[[ -f package-lock.json ]] && PM="npm"
```

### Phase 2: Environment Validation

**If project has `scripts/validate-env.sh`:**
```bash
./scripts/validate-env.sh --prod-only
```

**If Convex project:**
```bash
# Check production env vars exist
npx convex env list --prod | grep -E "STRIPE|CLERK|CONVEX" || echo "Missing critical vars"

# Check for trailing whitespace
npx convex env list --prod | while IFS= read -r line; do
  if [[ "$line" =~ [[:space:]]$ ]]; then
    echo "WARNING: Trailing whitespace in: $(echo "$line" | cut -d= -f1)"
  fi
done
```

**If Vercel project:**
```bash
# Check production env vars
vercel env ls --environment=production
```

### Phase 3: Git Status

```bash
# Check for uncommitted changes
git status --porcelain

# Check current branch
git branch --show-current

# Check if branch is up to date with remote
git fetch origin
git status -sb | head -1
```

### Phase 4: Quality Checks

**TypeScript:**
```bash
$PM tsc --noEmit
```

**Tests:**
```bash
$PM test --run
```

**Lint:**
```bash
$PM lint
```

**Secret Scan (if TruffleHog available):**
```bash
trufflehog filesystem . --only-verified --max-depth=3 --no-update 2>/dev/null
```

### Phase 5: Cross-Platform Parity

**Critical for Convex + Vercel projects:**
```bash
# CONVEX_WEBHOOK_TOKEN must exist on BOTH
echo "Checking CONVEX_WEBHOOK_TOKEN parity..."

convex_has=$(npx convex env list --prod 2>/dev/null | grep -c "^CONVEX_WEBHOOK_TOKEN=")
vercel_has=$(vercel env ls --environment=production 2>/dev/null | grep -c "CONVEX_WEBHOOK_TOKEN")

if [[ $convex_has -eq 0 ]]; then
  echo "MISSING: CONVEX_WEBHOOK_TOKEN on Convex prod"
fi

if [[ $vercel_has -eq 0 ]]; then
  echo "MISSING: CONVEX_WEBHOOK_TOKEN on Vercel prod"
fi

if [[ $convex_has -gt 0 ]] && [[ $vercel_has -gt 0 ]]; then
  echo "EXISTS on both (verify values match in Vercel Dashboard)"
fi
```

### Phase 6: Generate Report

```markdown
## Pre-Deployment Report

**Project**: [name]
**Branch**: [branch]
**Date**: [timestamp]

---

### Checks

| Check | Status | Notes |
|-------|--------|-------|
| Git status | ✅/❌ | Clean / [N] uncommitted |
| TypeScript | ✅/❌ | Compiles / [N] errors |
| Tests | ✅/❌ | Pass / [N] failures |
| Lint | ✅/❌ | Clean / [N] warnings |
| Env vars (local) | ✅/❌ | Set / [N] missing |
| Env vars (prod) | ✅/❌ | Set / [N] missing |
| Format validation | ✅/❌ | Valid / [N] issues |
| Cross-platform parity | ✅/❌ | Match / [N] mismatches |
| Secret scan | ✅/❌ | Clean / [N] secrets |

---

### Issues Found

1. **[BLOCKER/WARNING]**: [Description]
   - **Fix**: [Command or action]

---

### Deployment Command

If all checks pass:
```bash
# For Vercel
vercel --prod

# For Convex (manual push)
npx convex deploy --prod
```

---

**Decision**: ✅ READY TO DEPLOY / ❌ BLOCKED / ⚠️ PROCEED WITH CAUTION
```

## Quick Pre-Deploy Script

If project has `scripts/verify-deploy-ready.sh`:
```bash
./scripts/verify-deploy-ready.sh
```

Otherwise, run inline checks:
```bash
# Quick pre-deploy checklist
echo "=== Pre-Deploy Checklist ==="

# 1. Git status
[[ -z $(git status --porcelain) ]] && echo "✅ Git clean" || echo "⚠️ Uncommitted changes"

# 2. TypeScript
pnpm tsc --noEmit 2>/dev/null && echo "✅ TypeScript" || echo "❌ TypeScript errors"

# 3. Tests
pnpm test --run 2>/dev/null && echo "✅ Tests pass" || echo "❌ Tests fail"

# 4. Env validation
./scripts/validate-env.sh --prod-only 2>/dev/null && echo "✅ Env vars" || echo "❌ Env issues"

echo "=== Done ==="
```

## Philosophy

> **"Check config before code."**

Most production failures in external integrations are configuration errors, not code bugs:
- Missing env vars
- Trailing whitespace in secrets
- Tokens on one platform but not another
- Wrong webhook URLs

This command surfaces these issues BEFORE they cause production incidents.

## Related Commands

- `/stripe-check` - Deep dive into Stripe integration
- `/env-parity-check` - Focus on cross-platform token parity
- `/gates` - Quality infrastructure audit

---

*This command codifies lessons from production incidents. The few minutes spent checking saves hours of debugging.*
