#!/bin/bash
# List unresolved Sentry issues

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Default options
ENV_FILTER="production"
LIMIT=20
PROJECT_ARG=""
ORG_ARG=""
OUTPUT_JSON=false

HELP_TEXT="Usage: $(basename "$0") [OPTIONS]

List unresolved Sentry issues for a project.

Options:
  --env ENV        Environment filter (production, preview, development)
                   Default: production
  --limit N        Maximum issues to return (default: 20)
  --project SLUG   Override auto-detected project
  --org SLUG       Override organization
  --json           Output raw JSON instead of formatted table
  --help           Show this help message

Examples:
  $(basename "$0")                           # List production issues
  $(basename "$0") --env preview --limit 10  # List 10 preview issues
  $(basename "$0") --json | jq '.[]'         # Output as JSON"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --env)
      ENV_FILTER="$2"
      shift 2
      ;;
    --limit)
      LIMIT="$2"
      shift 2
      ;;
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
    *)
      die "Unknown option: $1. Use --help for usage."
      ;;
  esac
done

# Validate requirements
require_sentry_cli
require_auth

# Resolve org and project
ORG=$(resolve_org "$ORG_ARG")
PROJECT=$(resolve_project "$PROJECT_ARG")

info "Fetching issues for $ORG/$PROJECT (env: $ENV_FILTER, limit: $LIMIT)"
echo ""

# Use sentry-cli to list issues
if [ "$OUTPUT_JSON" = true ]; then
  # Use API for JSON output
  api_call GET "/projects/$ORG/$PROJECT/issues/?query=is:unresolved+environment:$ENV_FILTER&limit=$LIMIT" | parse_json '.'
else
  # Use sentry-cli for formatted output
  sentry-cli issues list \
    --org "$ORG" \
    --project "$PROJECT" \
    --status unresolved \
    --max-rows "$LIMIT" 2>/dev/null || {
      # Fallback to API if sentry-cli fails
      warn "sentry-cli failed, falling back to API"
      echo ""

      response=$(api_call GET "/projects/$ORG/$PROJECT/issues/?query=is:unresolved+environment:$ENV_FILTER&limit=$LIMIT")

      if ! echo "$response" | grep -q '"id"'; then
        die "Failed to fetch issues: $response"
      fi

      print_header

      echo "$response" | parse_json -r '.[] | [.shortId, .title, .count, .userCount, .lastSeen] | @tsv' | \
      while IFS=$'\t' read -r id title count users last_seen; do
        title_truncated=$(truncate "$title" 50)
        last_seen_fmt=$(format_time "$last_seen")
        printf "%-12s %-50s %8s %8s %12s\n" "$id" "$title_truncated" "$count" "$users" "$last_seen_fmt"
      done
    }
fi
