#!/usr/bin/env bash
set -eo pipefail

# Stripe webhook forwarding for Next.js API routes
# Auto-syncs ephemeral secret to .env.local

WEBHOOK_URL="localhost:3000/api/stripe/webhook"
ENV_FILE=".env.local"

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

if [[ -z "$SECRET" ]]; then
  echo "[Stripe] Could not get secret"
  tail -f /dev/null
fi

# Update .env.local
if grep -q "^STRIPE_WEBHOOK_SECRET=" "$ENV_FILE" 2>/dev/null; then
  # Use temp file for portable sed
  sed "s|^STRIPE_WEBHOOK_SECRET=.*|STRIPE_WEBHOOK_SECRET=$SECRET|" "$ENV_FILE" > "$ENV_FILE.tmp"
  mv "$ENV_FILE.tmp" "$ENV_FILE"
else
  echo "STRIPE_WEBHOOK_SECRET=$SECRET" >> "$ENV_FILE"
fi

echo "[Stripe] Updated $ENV_FILE with webhook secret"
echo "[Stripe] Note: Restart Next.js if already running to pick up new secret"
echo "[Stripe] Forwarding to $WEBHOOK_URL"
exec stripe -p sandbox listen --forward-to "$WEBHOOK_URL"
