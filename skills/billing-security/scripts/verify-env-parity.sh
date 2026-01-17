#!/bin/bash
#
# verify-env-parity.sh
#
# Verify that billing env vars are set on both Vercel and Convex.
# Prevents the "set on dev, forgot prod" problem.
#
# Usage: ./verify-env-parity.sh [--check-values]
# Exit codes: 0 = parity OK, 1 = mismatch found

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Billing-related env vars to check
REQUIRED_VARS=(
    "STRIPE_SECRET_KEY"
    "STRIPE_WEBHOOK_SECRET"
)

OPTIONAL_VARS=(
    "STRIPE_SYNC_SECRET"
    "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"
)

MISSING=0
WARNINGS=0

printf "Checking billing env var parity...\n\n"

# Check Vercel
printf "Checking Vercel (requires 'vercel' CLI)...\n"
if command -v vercel &> /dev/null; then
    VERCEL_VARS=$(vercel env ls 2>/dev/null | grep -E "^[A-Z_]+" | awk '{print $1}' || true)
else
    printf "${YELLOW}SKIP${NC}: vercel CLI not installed\n"
    VERCEL_VARS=""
fi

# Check Convex
printf "Checking Convex prod (requires 'convex' CLI)...\n"
if command -v npx &> /dev/null; then
    CONVEX_VARS=$(npx convex env list --prod 2>/dev/null | grep -E "^[A-Z_]+" | awk '{print $1}' || true)
else
    printf "${YELLOW}SKIP${NC}: npx not available\n"
    CONVEX_VARS=""
fi

printf "\n"

# Check required vars
for var in "${REQUIRED_VARS[@]}"; do
    IN_VERCEL=false
    IN_CONVEX=false

    if [[ -n "$VERCEL_VARS" ]] && printf '%s' "$VERCEL_VARS" | grep -q "^${var}$"; then
        IN_VERCEL=true
    fi

    if [[ -n "$CONVEX_VARS" ]] && printf '%s' "$CONVEX_VARS" | grep -q "^${var}$"; then
        IN_CONVEX=true
    fi

    if $IN_VERCEL && $IN_CONVEX; then
        printf "${GREEN}OK${NC}: %s (both platforms)\n" "$var"
    elif $IN_VERCEL && ! $IN_CONVEX; then
        printf "${RED}MISSING${NC}: %s (Vercel only, not on Convex prod)\n" "$var"
        MISSING=$((MISSING + 1))
    elif ! $IN_VERCEL && $IN_CONVEX; then
        printf "${RED}MISSING${NC}: %s (Convex only, not on Vercel)\n" "$var"
        MISSING=$((MISSING + 1))
    else
        printf "${RED}MISSING${NC}: %s (neither platform)\n" "$var"
        MISSING=$((MISSING + 1))
    fi
done

# Check optional vars (warn only)
for var in "${OPTIONAL_VARS[@]}"; do
    IN_VERCEL=false
    IN_CONVEX=false

    if [[ -n "$VERCEL_VARS" ]] && printf '%s' "$VERCEL_VARS" | grep -q "^${var}$"; then
        IN_VERCEL=true
    fi

    if [[ -n "$CONVEX_VARS" ]] && printf '%s' "$CONVEX_VARS" | grep -q "^${var}$"; then
        IN_CONVEX=true
    fi

    if $IN_VERCEL || $IN_CONVEX; then
        if $IN_VERCEL && $IN_CONVEX; then
            printf "${GREEN}OK${NC}: %s (both platforms)\n" "$var"
        else
            printf "${YELLOW}WARN${NC}: %s (only on one platform)\n" "$var"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
done

printf "\n"

# Summary
if [[ $MISSING -gt 0 ]]; then
    printf "${RED}FAIL${NC}: %d required env var(s) missing or mismatched\n" "$MISSING"
    printf "\nTo fix, set the missing vars:\n"
    printf "  Vercel: vercel env add <VAR_NAME>\n"
    printf "  Convex: npx convex env set --prod <VAR_NAME> <value>\n"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    printf "${YELLOW}WARN${NC}: %d optional env var(s) only on one platform\n" "$WARNINGS"
    exit 0
else
    printf "${GREEN}All billing env vars have parity.${NC}\n"
    exit 0
fi
