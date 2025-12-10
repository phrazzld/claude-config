#!/bin/bash
# Shared functions for Sentry CLI scripts
# Source this file: source "$(dirname "$0")/_common.sh"

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print error and exit
die() {
  echo -e "${RED}Error:${NC} $1" >&2
  exit 1
}

# Print warning
warn() {
  echo -e "${YELLOW}Warning:${NC} $1" >&2
}

# Print success
success() {
  echo -e "${GREEN}✓${NC} $1"
}

# Print info
info() {
  echo -e "${BLUE}→${NC} $1"
}

# Ensure sentry-cli is installed
require_sentry_cli() {
  if ! command -v sentry-cli &> /dev/null; then
    die "sentry-cli not found. Install with: curl -sL https://sentry.io/get-cli/ | bash"
  fi
}

# Ensure authentication token is available
require_auth() {
  # Try SENTRY_AUTH_TOKEN first, then SENTRY_MASTER_TOKEN
  if [ -z "${SENTRY_AUTH_TOKEN:-}" ]; then
    if [ -n "${SENTRY_MASTER_TOKEN:-}" ]; then
      export SENTRY_AUTH_TOKEN="$SENTRY_MASTER_TOKEN"
    else
      die "No Sentry auth token found. Set SENTRY_AUTH_TOKEN or SENTRY_MASTER_TOKEN"
    fi
  fi
}

# Resolve organization (from env or arg)
resolve_org() {
  local arg_org="${1:-}"

  if [ -n "$arg_org" ]; then
    echo "$arg_org"
    return
  fi

  if [ -n "${SENTRY_ORG:-}" ]; then
    echo "$SENTRY_ORG"
    return
  fi

  die "SENTRY_ORG not set. Pass --org or set SENTRY_ORG environment variable"
}

# Resolve project (from arg, .sentryclirc, .env.local, or env)
resolve_project() {
  local arg_project="${1:-}"

  # 1. CLI argument takes precedence
  if [ -n "$arg_project" ]; then
    echo "$arg_project"
    return
  fi

  # 2. Environment variable
  if [ -n "${SENTRY_PROJECT:-}" ]; then
    echo "$SENTRY_PROJECT"
    return
  fi

  # 3. .sentryclirc in current directory or parents
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/.sentryclirc" ]; then
      local project=$(grep "^project=" "$dir/.sentryclirc" 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'")
      if [ -n "$project" ]; then
        echo "$project"
        return
      fi
    fi
    dir=$(dirname "$dir")
  done

  # 4. .env.local in current directory
  if [ -f ".env.local" ]; then
    local project=$(grep "^SENTRY_PROJECT=" .env.local 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'")
    if [ -n "$project" ]; then
      echo "$project"
      return
    fi
  fi

  # 5. Not found
  die "SENTRY_PROJECT not found. Pass --project, set SENTRY_PROJECT, or add to .sentryclirc"
}

# Make API call with authentication
api_call() {
  local method="$1"
  local endpoint="$2"
  local data="${3:-}"

  require_auth

  local url="https://sentry.io/api/0${endpoint}"
  local args=(-s -X "$method" -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" -H "Content-Type: application/json")

  if [ -n "$data" ]; then
    args+=(-d "$data")
  fi

  curl "${args[@]}" "$url"
}

# Format timestamp to relative time
format_time() {
  local timestamp="$1"
  local now=$(date +%s)
  local then=$(date -jf "%Y-%m-%dT%H:%M:%S" "${timestamp%.*}" +%s 2>/dev/null || echo "$now")
  local diff=$((now - then))

  if [ $diff -lt 60 ]; then
    echo "${diff}s ago"
  elif [ $diff -lt 3600 ]; then
    echo "$((diff / 60))m ago"
  elif [ $diff -lt 86400 ]; then
    echo "$((diff / 3600))h ago"
  else
    echo "$((diff / 86400))d ago"
  fi
}

# Parse JSON with jq (with fallback message if jq not available)
parse_json() {
  if command -v jq &> /dev/null; then
    jq "$@"
  else
    warn "jq not installed, outputting raw JSON"
    cat
  fi
}

# Print table header
print_header() {
  printf "${BLUE}%-12s %-50s %8s %8s %12s${NC}\n" "ID" "TITLE" "EVENTS" "USERS" "LAST SEEN"
  printf "%-12s %-50s %8s %8s %12s\n" "------------" "--------------------------------------------------" "--------" "--------" "------------"
}

# Truncate string to max length
truncate() {
  local str="$1"
  local max="$2"
  if [ ${#str} -gt $max ]; then
    echo "${str:0:$((max-3))}..."
  else
    echo "$str"
  fi
}

# Show help for a command
show_help() {
  local script_name=$(basename "$0")
  local help_text="$1"

  echo "$help_text"
  echo ""
  echo "Environment variables:"
  echo "  SENTRY_AUTH_TOKEN    Sentry API token (or SENTRY_MASTER_TOKEN)"
  echo "  SENTRY_ORG           Organization slug"
  echo "  SENTRY_PROJECT       Project slug (auto-detected from .sentryclirc/.env.local)"
}
