#!/bin/bash
# Stripe Integration Audit Script
# Portable audit for Stripe integrations across project types
#
# Usage:
#   stripe_audit.sh                  # Full audit with Stripe CLI
#   stripe_audit.sh --local-only     # Skip Stripe CLI checks
#   stripe_audit.sh --quiet          # Minimal output (pass/fail only)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Flags
LOCAL_ONLY=false
QUIET=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --local-only)
      LOCAL_ONLY=true
      ;;
    --quiet)
      QUIET=true
      ;;
  esac
done

# Counters
PASS=0
WARN=0
FAIL=0

# Logging functions
log_pass() {
  ((PASS++))
  if [ "$QUIET" = false ]; then
    echo -e "${GREEN}✓${NC} $1"
  fi
}

log_warn() {
  ((WARN++))
  if [ "$QUIET" = false ]; then
    echo -e "${YELLOW}⚠${NC} $1"
  fi
}

log_fail() {
  ((FAIL++))
  echo -e "${RED}✗${NC} $1"
}

log_info() {
  if [ "$QUIET" = false ]; then
    echo -e "${BLUE}ℹ${NC} $1"
  fi
}

log_section() {
  if [ "$QUIET" = false ]; then
    echo ""
    echo -e "${BLUE}━━━ $1 ━━━${NC}"
  fi
}

# Detect project type
detect_project_type() {
  if [ -f "convex/_generated/api.d.ts" ] || [ -d "convex" ]; then
    echo "convex"
  elif [ -f "vercel.json" ] || [ -f ".vercel/project.json" ]; then
    echo "vercel"
  elif [ -f "package.json" ]; then
    echo "node"
  else
    echo "unknown"
  fi
}

# Check if Stripe SDK is installed
check_stripe_sdk() {
  log_section "Stripe SDK Detection"

  if grep -q '"stripe"' package.json 2>/dev/null; then
    local version
    version=$(grep '"stripe"' package.json | head -1 | sed 's/.*"\^*\([0-9.]*\)".*/\1/')
    log_pass "Stripe SDK found: v${version}"
    return 0
  else
    log_fail "Stripe SDK not found in package.json"
    return 1
  fi
}

# Check for hardcoded keys
check_hardcoded_keys() {
  log_section "Hardcoded Key Scan"

  local patterns=("sk_test_" "sk_live_" "pk_test_" "pk_live_" "whsec_")
  local found=false

  for pattern in "${patterns[@]}"; do
    local matches
    matches=$(grep -r "$pattern" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/ 2>/dev/null | grep -v node_modules | grep -v ".env" || true)
    if [ -n "$matches" ]; then
      log_fail "Hardcoded key pattern '$pattern' found in source code"
      if [ "$QUIET" = false ]; then
        echo "$matches" | head -3
      fi
      found=true
    fi
  done

  if [ "$found" = false ]; then
    log_pass "No hardcoded Stripe keys in source code"
  fi
}

# Check local env vars
check_local_env() {
  log_section "Local Environment (.env.local)"

  local required_vars=(
    "STRIPE_SECRET_KEY"
    "STRIPE_WEBHOOK_SECRET"
    "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"
  )

  if [ ! -f ".env.local" ]; then
    log_warn ".env.local not found (may be using different env file)"
    return
  fi

  for var in "${required_vars[@]}"; do
    if grep -q "^${var}=" .env.local 2>/dev/null; then
      log_pass "$var is set in .env.local"
    else
      log_warn "$var not found in .env.local"
    fi
  done
}

# Check Convex env vars
check_convex_env() {
  local deployment=$1
  local label=$2

  log_section "Convex Environment ($label)"

  if ! command -v npx &> /dev/null; then
    log_warn "npx not found, skipping Convex env check"
    return
  fi

  local cmd="npx convex env list"
  if [ -n "$deployment" ]; then
    cmd="CONVEX_DEPLOYMENT=$deployment npx convex env list"
  fi

  local env_output
  env_output=$(eval "$cmd" 2>/dev/null || echo "FAILED")

  if [ "$env_output" = "FAILED" ]; then
    log_fail "Could not list Convex env vars for $label"
    return
  fi

  local required_vars=(
    "STRIPE_SECRET_KEY"
    "STRIPE_WEBHOOK_SECRET"
  )

  for var in "${required_vars[@]}"; do
    if echo "$env_output" | grep -q "^$var"; then
      log_pass "$var is set in Convex $label"
    else
      log_fail "$var not set in Convex $label"
    fi
  done
}

# Check webhook signature verification in code
check_webhook_verification() {
  log_section "Webhook Security"

  local webhook_files
  webhook_files=$(grep -rl "stripe.webhooks.constructEvent\|constructEvent" --include="*.ts" --include="*.tsx" src/ convex/ 2>/dev/null || true)

  if [ -n "$webhook_files" ]; then
    log_pass "Webhook signature verification found"
    if [ "$QUIET" = false ]; then
      echo "$webhook_files" | head -3 | while read -r f; do
        log_info "  → $f"
      done
    fi
  else
    log_fail "No webhook signature verification found (stripe.webhooks.constructEvent)"
  fi

  # Check for raw body handling
  if grep -r "request.text()\|req.rawBody\|getRawBody" --include="*.ts" --include="*.tsx" src/ convex/ 2>/dev/null | grep -q .; then
    log_pass "Raw body handling found (required for webhook verification)"
  else
    log_warn "Raw body handling not detected (may cause signature verification issues)"
  fi
}

# Check for invalid mode-dependent params
check_mode_params() {
  log_section "Mode-Dependent Parameters"

  # Check for customer_creation in subscription mode (exclude test files and undefined assertions)
  local bad_pattern
  bad_pattern=$(grep -r "mode.*subscription" --include="*.ts" --include="*.tsx" -A5 src/ convex/ 2>/dev/null \
    | grep -v "\.test\." \
    | grep -v "\.spec\." \
    | grep -v "toBeUndefined" \
    | grep "customer_creation:" || true)

  if [ -n "$bad_pattern" ]; then
    log_fail "customer_creation may be used with subscription mode (invalid)"
    if [ "$QUIET" = false ]; then
      echo "$bad_pattern" | head -3
    fi
  else
    log_pass "No invalid mode-dependent parameters detected"
  fi
}

# Check health endpoint
check_health_endpoint() {
  log_section "Health Endpoint"

  local health_file
  health_file=$(find src/app/api -name "route.ts" -path "*health*" 2>/dev/null | head -1)

  if [ -n "$health_file" ]; then
    if grep -q "stripe\|STRIPE" "$health_file" 2>/dev/null; then
      log_pass "Health endpoint includes Stripe status check"
    else
      log_warn "Health endpoint exists but doesn't check Stripe configuration"
    fi
  else
    log_warn "No health endpoint found at /api/health"
  fi
}

# Stripe CLI checks
check_stripe_cli() {
  if [ "$LOCAL_ONLY" = true ]; then
    return
  fi

  log_section "Stripe CLI Checks"

  if ! command -v stripe &> /dev/null; then
    log_warn "Stripe CLI not installed, skipping Dashboard verification"
    log_info "Install: brew install stripe/stripe-cli/stripe"
    return
  fi

  # Check if authenticated
  if ! stripe config --list &>/dev/null; then
    log_warn "Stripe CLI not authenticated, skipping Dashboard verification"
    log_info "Run: stripe login"
    return
  fi

  # Check webhook endpoints
  log_info "Checking webhook endpoints..."
  local webhooks
  webhooks=$(stripe webhook_endpoints list --limit 5 2>/dev/null || echo "FAILED")

  if [ "$webhooks" = "FAILED" ]; then
    log_warn "Could not fetch webhook endpoints"
  else
    local count
    count=$(echo "$webhooks" | grep -c "url:" || echo "0")
    if [ "$count" -gt 0 ]; then
      log_pass "$count webhook endpoint(s) registered"
    else
      log_fail "No webhook endpoints registered in Stripe Dashboard"
    fi
  fi

  # Check recent events
  log_info "Checking recent events..."
  local events
  events=$(stripe events list --limit 5 2>/dev/null || echo "FAILED")

  if [ "$events" != "FAILED" ]; then
    log_pass "Recent events accessible via Stripe CLI"
  fi
}

# Verify price IDs
check_price_ids() {
  if [ "$LOCAL_ONLY" = true ]; then
    return
  fi

  log_section "Price ID Verification"

  if ! command -v stripe &> /dev/null; then
    return
  fi

  # Get price IDs from env
  local monthly_id=""
  local annual_id=""

  if [ -f ".env.local" ]; then
    monthly_id=$(grep "NEXT_PUBLIC_STRIPE_MONTHLY_PRICE_ID" .env.local 2>/dev/null | cut -d= -f2 || true)
    annual_id=$(grep "NEXT_PUBLIC_STRIPE_ANNUAL_PRICE_ID" .env.local 2>/dev/null | cut -d= -f2 || true)
  fi

  if [ -n "$monthly_id" ]; then
    if stripe prices retrieve "$monthly_id" &>/dev/null; then
      log_pass "Monthly price ID is valid: $monthly_id"
    else
      log_fail "Monthly price ID not found in Stripe: $monthly_id"
    fi
  fi

  if [ -n "$annual_id" ]; then
    if stripe prices retrieve "$annual_id" &>/dev/null; then
      log_pass "Annual price ID is valid: $annual_id"
    else
      log_fail "Annual price ID not found in Stripe: $annual_id"
    fi
  fi
}

# Main
main() {
  echo ""
  echo "╔════════════════════════════════════════╗"
  echo "║     Stripe Integration Audit           ║"
  echo "╚════════════════════════════════════════╝"

  PROJECT_TYPE=$(detect_project_type)
  log_info "Project type: $PROJECT_TYPE"

  # Run checks
  check_stripe_sdk || true
  check_hardcoded_keys
  check_local_env

  if [ "$PROJECT_TYPE" = "convex" ]; then
    check_convex_env "" "dev"

    # Try to find prod deployment
    if [ -f ".env.local" ]; then
      local prod_deployment
      prod_deployment=$(grep "CONVEX_DEPLOYMENT.*prod:" .env.local 2>/dev/null | cut -d= -f2 || true)
      if [ -z "$prod_deployment" ]; then
        # Try to infer from convex.json or prompt
        log_info "Tip: Set CONVEX_DEPLOYMENT=prod:xxx to check prod env vars"
      else
        check_convex_env "$prod_deployment" "prod"
      fi
    fi
  fi

  check_webhook_verification
  check_mode_params
  check_health_endpoint
  check_stripe_cli
  check_price_ids

  # Summary
  echo ""
  echo "╔════════════════════════════════════════╗"
  echo "║     Audit Summary                      ║"
  echo "╚════════════════════════════════════════╝"
  echo -e "  ${GREEN}Passed:${NC}  $PASS"
  echo -e "  ${YELLOW}Warnings:${NC} $WARN"
  echo -e "  ${RED}Failed:${NC}  $FAIL"
  echo ""

  if [ "$FAIL" -gt 0 ]; then
    echo -e "${RED}Audit failed with $FAIL issue(s)${NC}"
    exit 1
  elif [ "$WARN" -gt 0 ]; then
    echo -e "${YELLOW}Audit passed with $WARN warning(s)${NC}"
    exit 0
  else
    echo -e "${GREEN}Audit passed!${NC}"
    exit 0
  fi
}

main
