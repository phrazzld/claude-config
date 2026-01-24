#!/bin/bash
# Check Sentry for unresolved issues
# Wraps sentry-observability/scripts/triage_score.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Options
OUTPUT_FORMAT="${1:-summary}"  # summary | json | detail
PROJECT="${SENTRY_PROJECT:-$(detect_project)}"
LIMIT="${TRIAGE_SENTRY_LIMIT:-5}"

# Path to existing sentry script
TRIAGE_SCRIPT="$HOME/.claude/skills/sentry-observability/scripts/triage_score.sh"

if [ ! -x "$TRIAGE_SCRIPT" ]; then
  echo "SENTRY"
  status_warn "triage_score.sh not found. Install sentry-observability skill."
  exit 0
fi

# Check for auth
if [ -z "${SENTRY_AUTH_TOKEN:-}" ] && [ -z "${SENTRY_MASTER_TOKEN:-}" ]; then
  echo "SENTRY"
  status_warn "No SENTRY_AUTH_TOKEN. Set env var or run 'sentry-cli login'."
  exit 0
fi

# Get scored issues as JSON
issues_json=$("$TRIAGE_SCRIPT" --limit "$LIMIT" --json 2>/dev/null || echo "[]")

# Parse results
if [ "$issues_json" = "[]" ] || [ -z "$issues_json" ]; then
  echo "SENTRY ($PROJECT)"
  status_ok "No unresolved issues"
  exit 0
fi

# Count issues
issue_count=$(echo "$issues_json" | jq 'length' 2>/dev/null || echo "0")

if [ "$issue_count" -eq 0 ]; then
  echo "SENTRY ($PROJECT)"
  status_ok "No unresolved issues"
  exit 0
fi

# Get top issue details
top_issue=$(echo "$issues_json" | jq -r '.[0]' 2>/dev/null)
top_id=$(echo "$top_issue" | jq -r '.id // "unknown"')
top_title=$(echo "$top_issue" | jq -r '.title // "unknown"' | head -c 50)
top_score=$(echo "$top_issue" | jq -r '.score // 0')
top_users=$(echo "$top_issue" | jq -r '.users // 0')

# Determine severity based on score
if [ "${top_score%.*}" -gt 100 ]; then
  severity="CRITICAL"
elif [ "${top_score%.*}" -gt 50 ]; then
  severity="HIGH"
else
  severity="MEDIUM"
fi

case "$OUTPUT_FORMAT" in
  json)
    echo "$issues_json"
    ;;
  detail)
    echo "SENTRY ($PROJECT)"
    if [ "$severity" = "CRITICAL" ]; then
      status_critical "$issue_count unresolved issues"
    else
      status_warn "$issue_count unresolved issues"
    fi
    echo "  Top: $top_id \"$top_title\" (Score: $top_score, $top_users users)"
    echo ""
    echo "  All issues:"
    echo "$issues_json" | jq -r '.[] | "    - \(.id): \(.title | .[0:40]) (score: \(.score), users: \(.users))"'
    ;;
  *)
    # summary (default)
    echo "SENTRY ($PROJECT)"
    if [ "$severity" = "CRITICAL" ]; then
      status_critical "$issue_count unresolved issues"
    else
      status_warn "$issue_count unresolved issues"
    fi
    echo "  Top: $top_id \"$top_title\" (Score: ${top_score%.*}, $top_users users)"
    ;;
esac
