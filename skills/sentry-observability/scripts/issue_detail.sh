#!/bin/bash
# Get full context for a specific Sentry issue

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Default options
ISSUE_ID=""
PROJECT_ARG=""
ORG_ARG=""
OUTPUT_JSON=false

HELP_TEXT="Usage: $(basename "$0") <ISSUE_ID> [OPTIONS]

Get full context for a specific Sentry issue.

Arguments:
  ISSUE_ID         The issue ID (e.g., PROJECT-123 or numeric ID)

Options:
  --project SLUG   Override auto-detected project
  --org SLUG       Override organization
  --json           Output raw JSON
  --help           Show this help message

Examples:
  $(basename "$0") MYAPP-123
  $(basename "$0") 12345678 --json
  $(basename "$0") MYAPP-123 --project my-project"

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
    --json)
      OUTPUT_JSON=true
      shift
      ;;
    --help|-h)
      show_help "$HELP_TEXT"
      exit 0
      ;;
    -*)
      die "Unknown option: $1. Use --help for usage."
      ;;
    *)
      if [ -z "$ISSUE_ID" ]; then
        ISSUE_ID="$1"
      else
        die "Unexpected argument: $1"
      fi
      shift
      ;;
  esac
done

# Validate
if [ -z "$ISSUE_ID" ]; then
  die "Issue ID is required. Use --help for usage."
fi

require_auth

# Resolve org if needed
ORG=$(resolve_org "$ORG_ARG" 2>/dev/null || echo "")

info "Fetching details for issue: $ISSUE_ID"
echo ""

# Fetch issue details
issue_response=$(api_call GET "/issues/$ISSUE_ID/")

if echo "$issue_response" | grep -q '"detail"'; then
  die "Failed to fetch issue: $(echo "$issue_response" | parse_json -r '.detail')"
fi

# Fetch latest event
event_response=$(api_call GET "/issues/$ISSUE_ID/events/latest/")

if [ "$OUTPUT_JSON" = true ]; then
  # Combine and output JSON
  echo "$issue_response" | parse_json --arg event "$event_response" '. + {latestEvent: ($event | fromjson)}'
else
  # Format human-readable output
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║                    Issue Details                             ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""

  # Basic info
  title=$(echo "$issue_response" | parse_json -r '.title')
  short_id=$(echo "$issue_response" | parse_json -r '.shortId')
  status=$(echo "$issue_response" | parse_json -r '.status')
  level=$(echo "$issue_response" | parse_json -r '.level')
  first_seen=$(echo "$issue_response" | parse_json -r '.firstSeen')
  last_seen=$(echo "$issue_response" | parse_json -r '.lastSeen')
  count=$(echo "$issue_response" | parse_json -r '.count')
  user_count=$(echo "$issue_response" | parse_json -r '.userCount')

  echo -e "${BLUE}ID:${NC}          $short_id"
  echo -e "${BLUE}Title:${NC}       $title"
  echo -e "${BLUE}Status:${NC}      $status"
  echo -e "${BLUE}Level:${NC}       $level"
  echo ""
  echo -e "${BLUE}First Seen:${NC}  $first_seen"
  echo -e "${BLUE}Last Seen:${NC}   $last_seen"
  echo ""
  echo -e "${BLUE}Events:${NC}      $count"
  echo -e "${BLUE}Users:${NC}       $user_count"
  echo ""

  # Stack trace (from latest event)
  if echo "$event_response" | grep -q '"entries"'; then
    echo "Stack Trace"
    echo "-----------"
    echo "$event_response" | parse_json -r '
      .entries[]? |
      select(.type == "exception") |
      .data.values[]? |
      .stacktrace.frames[-3:][]? |
      "\(.filename // "unknown"):\(.lineno // "?") in \(.function // "unknown")"
    ' 2>/dev/null | tail -5 || echo "(No stack trace available)"
    echo ""
  fi

  # Breadcrumbs
  if echo "$event_response" | grep -q '"breadcrumbs"'; then
    echo "Recent Breadcrumbs"
    echo "------------------"
    echo "$event_response" | parse_json -r '
      .entries[]? |
      select(.type == "breadcrumbs") |
      .data.values[-5:][]? |
      "[\(.category // "unknown")] \(.message // .data // "no message")"
    ' 2>/dev/null | tail -5 || echo "(No breadcrumbs available)"
    echo ""
  fi

  # Tags
  if echo "$issue_response" | grep -q '"tags"'; then
    echo "Tags"
    echo "----"
    echo "$issue_response" | parse_json -r '.tags[]? | "\(.key): \(.value)"' 2>/dev/null | head -10 || echo "(No tags)"
    echo ""
  fi

  # Link to Sentry
  permalink=$(echo "$issue_response" | parse_json -r '.permalink // empty')
  if [ -n "$permalink" ]; then
    echo -e "${BLUE}View in Sentry:${NC} $permalink"
  fi
fi
