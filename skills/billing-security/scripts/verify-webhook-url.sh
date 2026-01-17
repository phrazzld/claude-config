#!/bin/bash
#
# verify-webhook-url.sh
#
# Verify that a webhook URL is reachable and doesn't redirect.
# Stripe does NOT follow redirects for POST requests.
#
# Usage: ./verify-webhook-url.sh <url>
# Exit codes: 0 = OK, 1 = FAIL

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ $# -lt 1 ]]; then
    printf "Usage: %s <webhook_url>\n" "$0"
    printf "Example: %s https://www.example.com/api/webhooks/stripe\n" "$0"
    exit 1
fi

URL="$1"

printf "Verifying webhook URL: %s\n\n" "$URL"

# Check 1: URL format
if [[ ! "$URL" =~ ^https:// ]]; then
    printf "${RED}FAIL${NC}: URL must use HTTPS\n"
    exit 1
fi

# Check 2: HTTP status (check for redirects)
printf "Checking for redirects...\n"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -I -X POST "$URL" 2>/dev/null || printf "000")

if [[ "$HTTP_STATUS" =~ ^3 ]]; then
    printf "${RED}FAIL${NC}: URL returns %s (redirect)\n" "$HTTP_STATUS"
    printf "\nStripe does NOT follow redirects for POST webhooks!\n"
    printf "The webhook will silently fail.\n\n"

    # Show where it redirects to
    REDIRECT_URL=$(curl -s -I -X POST "$URL" 2>/dev/null | grep -i "^location:" | cut -d' ' -f2 | tr -d '\r')
    if [[ -n "$REDIRECT_URL" ]]; then
        printf "Redirects to: %s\n" "$REDIRECT_URL"
        printf "Use the canonical URL in your Stripe webhook configuration.\n"
    fi
    exit 1
elif [[ "$HTTP_STATUS" == "000" ]]; then
    printf "${RED}FAIL${NC}: Could not connect to URL\n"
    printf "Check that the domain is correct and the server is running.\n"
    exit 1
elif [[ "$HTTP_STATUS" =~ ^[45] ]]; then
    printf "${GREEN}OK${NC}: URL returns %s (no redirect)\n" "$HTTP_STATUS"
    printf "4xx/5xx is expected for POST without valid Stripe signature.\n"
else
    printf "${YELLOW}WARN${NC}: URL returns %s\n" "$HTTP_STATUS"
    printf "Expected 4xx or 5xx for POST without signature.\n"
fi

# Check 3: Verify it's a webhook endpoint path
if [[ ! "$URL" =~ /webhook ]]; then
    printf "${YELLOW}WARN${NC}: URL doesn't contain 'webhook' in path\n"
    printf "Are you sure this is the correct endpoint?\n"
fi

printf "\n${GREEN}Webhook URL verified.${NC}\n"
exit 0
