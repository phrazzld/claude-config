#!/bin/bash
# Verify Sentry configuration health in current project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Default options
PROJECT_ARG=""
ORG_ARG=""
FIX_MODE=false

HELP_TEXT="Usage: $(basename "$0") [OPTIONS]

Verify Sentry configuration health in the current project.

Options:
  --project SLUG   Override auto-detected project
  --org SLUG       Override organization
  --fix            Attempt to fix common issues (not yet implemented)
  --help           Show this help message

Checks performed:
  1. SENTRY_AUTH_TOKEN set and valid
  2. SENTRY_ORG accessible
  3. SENTRY_PROJECT exists and accessible
  4. DSN configured in .env.local
  5. Source map uploads (recent releases)
  6. Test error route exists
  7. Recent events in project

Examples:
  $(basename "$0")
  $(basename "$0") --project my-project"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --project)
      PROJECT_ARG="$2"
      shift 2
      ;;
    --org)
      ORG_ARG="$2"
      shift 2
      ;;
    --fix)
      FIX_MODE=true
      shift
      ;;
    --help|-h)
      show_help "$HELP_TEXT"
      exit 0
      ;;
    *)
      die "Unknown option: $1. Use --help for usage."
      ;;
  esac
done

# Results tracking
declare -A results
passed=0
failed=0
warnings=0

check_pass() {
  local name="$1"
  local detail="${2:-}"
  results[$name]="pass"
  ((passed++))
  if [ -n "$detail" ]; then
    success "$name: $detail"
  else
    success "$name"
  fi
}

check_fail() {
  local name="$1"
  local detail="${2:-}"
  results[$name]="fail"
  ((failed++))
  if [ -n "$detail" ]; then
    echo -e "${RED}✗ $name:${NC} $detail"
  else
    echo -e "${RED}✗ $name${NC}"
  fi
}

check_warn() {
  local name="$1"
  local detail="${2:-}"
  results[$name]="warn"
  ((warnings++))
  if [ -n "$detail" ]; then
    echo -e "${YELLOW}⚠ $name:${NC} $detail"
  else
    echo -e "${YELLOW}⚠ $name${NC}"
  fi
}

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║             Sentry Configuration Health Check                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check 1: Auth Token
echo "Checking authentication..."
if [ -n "${SENTRY_AUTH_TOKEN:-}" ] || [ -n "${SENTRY_MASTER_TOKEN:-}" ]; then
  # Try to validate token by making an API call
  token="${SENTRY_AUTH_TOKEN:-$SENTRY_MASTER_TOKEN}"
  export SENTRY_AUTH_TOKEN="$token"

  response=$(curl -s -H "Authorization: Bearer $token" "https://sentry.io/api/0/")
  if echo "$response" | grep -q '"user"'; then
    user=$(echo "$response" | parse_json -r '.user.name // .user.email // "unknown"')
    check_pass "Auth Token" "Valid (user: $user)"
  else
    check_fail "Auth Token" "Token exists but appears invalid"
  fi
else
  check_fail "Auth Token" "SENTRY_AUTH_TOKEN or SENTRY_MASTER_TOKEN not set"
fi

# Check 2: Organization
echo "Checking organization access..."
ORG="${SENTRY_ORG:-}"
if [ -n "$ORG_ARG" ]; then
  ORG="$ORG_ARG"
fi

if [ -n "$ORG" ]; then
  response=$(api_call GET "/organizations/$ORG/" 2>/dev/null || echo '{"error": true}')
  if echo "$response" | grep -q '"slug"'; then
    org_name=$(echo "$response" | parse_json -r '.name // .slug')
    check_pass "Organization" "$ORG ($org_name)"
  else
    check_fail "Organization" "Cannot access org: $ORG"
  fi
else
  check_fail "Organization" "SENTRY_ORG not set"
fi

# Check 3: Project
echo "Checking project access..."
PROJECT=""
if [ -n "$PROJECT_ARG" ]; then
  PROJECT="$PROJECT_ARG"
else
  PROJECT=$(resolve_project "" 2>/dev/null || echo "")
fi

if [ -n "$PROJECT" ] && [ -n "$ORG" ]; then
  response=$(api_call GET "/projects/$ORG/$PROJECT/" 2>/dev/null || echo '{"error": true}')
  if echo "$response" | grep -q '"slug"'; then
    project_name=$(echo "$response" | parse_json -r '.name // .slug')
    check_pass "Project" "$PROJECT ($project_name)"
  else
    check_fail "Project" "Cannot access project: $ORG/$PROJECT"
  fi
elif [ -z "$PROJECT" ]; then
  check_warn "Project" "Could not auto-detect. Set SENTRY_PROJECT or create .sentryclirc"
fi

# Check 4: DSN in environment
echo "Checking DSN configuration..."
dsn_found=false
for env_file in ".env.local" ".env" ".env.development"; do
  if [ -f "$env_file" ]; then
    if grep -q "SENTRY_DSN=.\+\|NEXT_PUBLIC_SENTRY_DSN=.\+" "$env_file" 2>/dev/null; then
      dsn_found=true
      check_pass "DSN Config" "Found in $env_file"
      break
    fi
  fi
done

if [ "$dsn_found" = false ]; then
  check_fail "DSN Config" "SENTRY_DSN not found in .env.local or .env"
fi

# Check 5: Source Maps (recent releases)
echo "Checking source map uploads..."
if [ -n "$ORG" ] && [ -n "$PROJECT" ]; then
  response=$(api_call GET "/organizations/$ORG/releases/?project=$PROJECT&per_page=5" 2>/dev/null || echo '[]')
  release_count=$(echo "$response" | parse_json 'length' 2>/dev/null || echo "0")

  if [ "$release_count" -gt 0 ]; then
    latest=$(echo "$response" | parse_json -r '.[0].version // "unknown"')
    check_pass "Source Maps" "Found $release_count recent releases (latest: $latest)"
  else
    check_warn "Source Maps" "No releases found. Source maps may not be uploading."
  fi
else
  check_warn "Source Maps" "Skipped (project not configured)"
fi

# Check 6: Test error route
echo "Checking test error route..."
if [ -f "app/test-error/route.ts" ] || [ -f "app/test-error/route.js" ]; then
  check_pass "Test Route" "app/test-error/route.ts exists"
elif [ -f "pages/api/test-error.ts" ] || [ -f "pages/api/test-error.js" ]; then
  check_pass "Test Route" "pages/api/test-error exists"
else
  check_warn "Test Route" "No test error route found. Create one to verify setup."
fi

# Check 7: Recent events
echo "Checking for recent events..."
if [ -n "$ORG" ] && [ -n "$PROJECT" ]; then
  response=$(api_call GET "/projects/$ORG/$PROJECT/issues/?limit=1" 2>/dev/null || echo '[]')
  if echo "$response" | grep -q '"id"'; then
    check_pass "Events" "Project is receiving events"
  else
    check_warn "Events" "No recent issues found. This could be good (no errors) or bad (not configured)."
  fi
else
  check_warn "Events" "Skipped (project not configured)"
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo -e "Results: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC}, ${YELLOW}$warnings warnings${NC}"
echo ""

if [ $failed -gt 0 ]; then
  echo "Issues detected. Fix the failed checks above."
  echo ""
  echo "Common fixes:"
  echo "  - Auth: source ~/.secrets or export SENTRY_AUTH_TOKEN=..."
  echo "  - Org/Project: export SENTRY_ORG=... SENTRY_PROJECT=..."
  echo "  - DSN: Add SENTRY_DSN to .env.local"
  echo "  - Source maps: Install Vercel Integration"
  exit 1
elif [ $warnings -gt 0 ]; then
  echo "Configuration looks mostly good, but has some warnings."
  exit 0
else
  echo "All checks passed! Sentry is properly configured."
  exit 0
fi
