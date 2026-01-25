#!/bin/bash
# Show which Stripe environment is configured for each context
echo "=== Stripe Environment Map ==="
echo ""
echo "CLI Profiles:"
echo "  sandbox:    $(stripe -p sandbox config --list 2>&1 | grep account_id | cut -d= -f2 || echo 'not configured')"
echo "  production: $(stripe -p production config --list 2>&1 | grep account_id | cut -d= -f2 || echo 'not configured')"
echo ""
echo "Local Environment (.env.local):"
if [ -f .env.local ]; then
  KEY=$(grep '^STRIPE_SECRET_KEY' .env.local 2>/dev/null | cut -d= -f2)
  if [ -n "$KEY" ]; then
    echo "  STRIPE_SECRET_KEY: ${KEY:0:20}..."
    # Determine if it's sandbox or production based on key pattern
    if [[ "$KEY" =~ ^sk_test_51SV2rGD ]]; then
      echo "  Environment: SANDBOX"
    elif [[ "$KEY" =~ ^sk_test_51SV2rAD ]]; then
      echo "  Environment: MAIN ACCOUNT (test mode)"
    elif [[ "$KEY" =~ ^sk_live_ ]]; then
      echo "  Environment: PRODUCTION (live!)"
    else
      echo "  Environment: UNKNOWN"
    fi
  else
    echo "  STRIPE_SECRET_KEY: not set"
  fi
else
  echo "  .env.local not found"
fi
