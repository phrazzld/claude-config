#!/bin/bash
# Shared functions for triage scripts
# Source this file: source "$(dirname "$0")/_common.sh"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auto-source secrets (credentials for Sentry, Vercel, etc.)
[ -f ~/.secrets ] && source ~/.secrets 2>/dev/null

# Import helpers from sentry-observability if available
SENTRY_COMMON="$HOME/.claude/skills/sentry-observability/scripts/_common.sh"
if [ -f "$SENTRY_COMMON" ]; then
  source "$SENTRY_COMMON"
else
  # Fallback definitions
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  CYAN='\033[0;36m'
  NC='\033[0m'

  die() { echo -e "${RED}Error:${NC} $1" >&2; exit 1; }
  warn() { echo -e "${YELLOW}Warning:${NC} $1" >&2; }
  success() { echo -e "${GREEN}OK${NC} $1"; }
  info() { echo -e "${BLUE}->>${NC} $1"; }
fi

# Additional colors
CYAN='\033[0;36m'
BOLD='\033[1m'

# Status indicators
status_ok() {
  echo -e "  ${GREEN}[OK]${NC} $1"
}

status_warn() {
  echo -e "  ${YELLOW}[WARN]${NC} $1"
}

status_critical() {
  echo -e "  ${RED}[CRITICAL]${NC} $1"
}

# Print section header
print_section() {
  local title="$1"
  echo ""
  echo -e "${BOLD}${title}${NC}"
}

# Get current timestamp
timestamp() {
  date "+%Y-%m-%d %H:%M"
}

# Check if command exists
has_command() {
  command -v "$1" &> /dev/null
}

# Auto-detect project from current directory
detect_project() {
  # Try .sentryclirc
  if [ -f ".sentryclirc" ]; then
    local project=$(grep "^project=" .sentryclirc 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'")
    if [ -n "$project" ]; then
      echo "$project"
      return
    fi
  fi

  # Try .env.local
  if [ -f ".env.local" ]; then
    local project=$(grep "^SENTRY_PROJECT=" .env.local 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'")
    if [ -n "$project" ]; then
      echo "$project"
      return
    fi
  fi

  # Try package.json name field
  if [ -f "package.json" ] && has_command jq; then
    local name=$(jq -r '.name // empty' package.json 2>/dev/null)
    if [ -n "$name" ]; then
      echo "$name"
      return
    fi
  fi

  # Fallback to directory name
  basename "$PWD"
}

# Detect production URL for health checks
detect_prod_url() {
  # Try .env.local NEXT_PUBLIC_URL
  if [ -f ".env.local" ]; then
    local url=$(grep "^NEXT_PUBLIC_URL=" .env.local 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'")
    if [ -n "$url" ]; then
      echo "$url"
      return
    fi
  fi

  # Try vercel.json or package.json homepage
  if [ -f "package.json" ] && has_command jq; then
    local homepage=$(jq -r '.homepage // empty' package.json 2>/dev/null)
    if [ -n "$homepage" ]; then
      echo "$homepage"
      return
    fi
  fi

  # No URL detected
  echo ""
}

# Format duration in human-readable form
format_duration() {
  local seconds="$1"
  if [ "$seconds" -lt 60 ]; then
    echo "${seconds}s"
  elif [ "$seconds" -lt 3600 ]; then
    echo "$((seconds / 60))m $((seconds % 60))s"
  else
    echo "$((seconds / 3600))h $((seconds % 3600 / 60))m"
  fi
}

# Parallel execution helper (waits for all background jobs)
wait_all() {
  local pids=("$@")
  local failed=0
  for pid in "${pids[@]}"; do
    wait "$pid" || ((failed++))
  done
  return $failed
}
