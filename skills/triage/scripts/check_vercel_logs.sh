#!/bin/bash
# Check Vercel logs for recent errors
# Uses Vercel API directly (more reliable than CLI)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"
set +e  # Don't exit on errors

# Source secrets if available
[ -f ~/.secrets ] && source ~/.secrets 2>/dev/null

# Options
OUTPUT_FORMAT="${1:-summary}"  # summary | json | detail
SINCE="${TRIAGE_VERCEL_SINCE:-10m}"

# Check for token
if [ -z "${VERCEL_TOKEN:-}" ]; then
  echo "VERCEL LOGS"
  echo "  [SKIP] VERCEL_TOKEN not set"
  exit 0
fi

# Get project info
PROJECT_ID=""
TEAM_ID=""

if [ -f ".vercel/project.json" ]; then
  PROJECT_ID=$(jq -r '.projectId // empty' .vercel/project.json 2>/dev/null)
  # Team ID might be in org settings
  TEAM_ID=$(jq -r '.orgId // empty' .vercel/project.json 2>/dev/null)
fi

if [ -z "$PROJECT_ID" ]; then
  echo "VERCEL LOGS"
  echo "  [SKIP] Not a Vercel project (no .vercel/project.json)"
  exit 0
fi

# Calculate since timestamp (convert to Unix ms)
case "$SINCE" in
  *m) minutes="${SINCE%m}"; since_ts=$(($(date +%s) - minutes * 60))000 ;;
  *h) hours="${SINCE%h}"; since_ts=$(($(date +%s) - hours * 3600))000 ;;
  *d) days="${SINCE%d}"; since_ts=$(($(date +%s) - days * 86400))000 ;;
  *)  since_ts=$(($(date +%s) - 600))000 ;;  # default 10 minutes
esac

# Parse events for errors
if ! has_command jq; then
  echo "VERCEL LOGS"
  status_warn "jq not installed, cannot parse logs"
  exit 0
fi

# Step 1: Get recent deployments for the project
# Note: /v2/projects/{id}/events doesn't exist - must fetch via deployments
DEPLOY_URL="https://api.vercel.com/v6/deployments?projectId=$PROJECT_ID&limit=5"
[ -n "$TEAM_ID" ] && DEPLOY_URL="$DEPLOY_URL&teamId=$TEAM_ID"

deploy_response=$(curl -s -H "Authorization: Bearer $VERCEL_TOKEN" "$DEPLOY_URL" 2>&1)

if echo "$deploy_response" | grep -q '"error"'; then
  error_msg=$(echo "$deploy_response" | jq -r '.error.message // .error // "Unknown error"' 2>/dev/null)
  echo "VERCEL LOGS"
  status_warn "API error fetching deployments: $error_msg"
  exit 0
fi

# Extract deployment UIDs
deployment_uids=$(echo "$deploy_response" | jq -r '.deployments[]?.uid // empty' 2>/dev/null)

if [ -z "$deployment_uids" ]; then
  echo "VERCEL LOGS"
  status_ok "No deployments found"
  exit 0
fi

# Step 2: Fetch events from recent deployments and aggregate
all_events="[]"
for uid in $deployment_uids; do
  EVENT_URL="https://api.vercel.com/v2/deployments/$uid/events?limit=50"
  [ -n "$TEAM_ID" ] && EVENT_URL="$EVENT_URL&teamId=$TEAM_ID"

  event_response=$(curl -s -H "Authorization: Bearer $VERCEL_TOKEN" "$EVENT_URL" 2>&1)

  # Skip if error or no events
  if echo "$event_response" | grep -q '"error"'; then
    continue
  fi

  # Merge events, filtering by timestamp
  deployment_events=$(echo "$event_response" | jq --argjson since "$since_ts" \
    '[.[] | select(.created >= $since)]' 2>/dev/null || echo "[]")

  all_events=$(echo "$all_events $deployment_events" | jq -s 'add | sort_by(-.created)' 2>/dev/null || echo "[]")
done

events="$all_events"

if [ "$events" = "null" ] || [ "$events" = "[]" ]; then
  echo "VERCEL LOGS"
  status_ok "No events in last $SINCE"
  exit 0
fi

# Filter for errors (deployment failures, function errors, stderr, etc.)
error_count=$(echo "$events" | jq '[.[] | select(.type == "error" or .type == "stderr" or (.payload.statusCode // 0) >= 500)] | length' 2>/dev/null || echo "0")
total_count=$(echo "$events" | jq 'length' 2>/dev/null || echo "0")

case "$OUTPUT_FORMAT" in
  json)
    cat <<EOF
{
  "total_events": $total_count,
  "errors": $error_count,
  "period": "$SINCE"
}
EOF
    ;;
  detail)
    echo "VERCEL LOGS"
    if [ "$error_count" -gt 0 ]; then
      status_critical "$error_count errors in last $SINCE"
      echo ""
      echo "  Recent errors:"
      echo "$events" | jq -r '.[] | select(.type == "error" or .type == "stderr" or (.payload.statusCode // 0) >= 500) | "    [\(.type)] \(.payload.text // .payload.path // .payload.name // "unknown" | .[0:80])"' 2>/dev/null | head -5
    else
      status_ok "No errors in last $SINCE ($total_count events)"
    fi
    ;;
  *)
    # summary (default)
    echo "VERCEL LOGS"
    if [ "$error_count" -gt 0 ]; then
      status_critical "$error_count errors in last $SINCE"
    else
      status_ok "No errors in last $SINCE"
    fi
    ;;
esac

# Exit code
if [ "$error_count" -gt 0 ]; then
  exit 2
fi
exit 0
