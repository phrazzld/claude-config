#!/usr/bin/env bash
set -eo pipefail

# Stripe webhook forwarding for Convex HTTP endpoints
# Auto-syncs ephemeral secret to Convex environment

WEBHOOK_PATH="/stripe/webhook"

# Derive Convex site URL
if [ -f .env.local ]; then
  CONVEX_URL=$(grep -m1 '^NEXT_PUBLIC_CONVEX_URL=' .env.local | cut -d= -f2 | tr -d '"' | tr -d "'")
  WEBHOOK_URL=$(echo "$CONVEX_URL" | sed 's/\.cloud/.site/')$WEBHOOK_PATH
else
  echo "[Stripe] Error: .env.local not found"
  exit 1
fi

# Check Stripe CLI
if ! command -v stripe &> /dev/null; then
  echo "[Stripe] CLI not installed. Install: brew install stripe/stripe-cli/stripe"
  tail -f /dev/null  # Keep process alive for concurrently
fi

# Check login
if ! stripe config --list &> /dev/null 2>&1; then
  echo "[Stripe] Not logged in. Run: stripe login"
  tail -f /dev/null
fi

echo "[Stripe] Getting webhook secret..."
SECRET=$(stripe -p sandbox listen --forward-to "$WEBHOOK_URL" --print-secret 2>/dev/null)

if [[ -n "$SECRET" ]]; then
  npx convex env set STRIPE_WEBHOOK_SECRET "$SECRET" > /dev/null 2>&1
  echo "[Stripe] Secret synced to Convex"
fi

echo "[Stripe] Forwarding to $WEBHOOK_URL"
exec stripe -p sandbox listen --forward-to "$WEBHOOK_URL"
