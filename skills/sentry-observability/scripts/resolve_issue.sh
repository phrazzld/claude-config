#!/bin/bash
# Mark Sentry issue as resolved

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Default options
ISSUE_ID=""
COMMIT_SHA=""
RELEASE_VERSION=""
PROJECT_ARG=""

HELP_TEXT="Usage: $(basename "$0") <ISSUE_ID> [OPTIONS]

Mark a Sentry issue as resolved.

Arguments:
  ISSUE_ID           The issue ID (e.g., PROJECT-123 or numeric ID)

Options:
  --commit SHA       Associate resolution with a commit
  --release VERSION  Associate resolution with a release version
  --project SLUG     Override auto-detected project
  --help             Show this help message

Examples:
  $(basename "$0") MYAPP-123
  $(basename "$0") MYAPP-123 --commit abc123
  $(basename "$0") MYAPP-123 --release v1.2.3"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --commit)
      COMMIT_SHA="$2"
      shift 2
      ;;
    --release)
      RELEASE_VERSION="$2"
      shift 2
      ;;
    --project)
      PROJECT_ARG="$2"
      shift 2
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

info "Resolving issue: $ISSUE_ID"

# Build payload
PAYLOAD='{"status": "resolved"}'

if [ -n "$COMMIT_SHA" ]; then
  PAYLOAD=$(echo "$PAYLOAD" | parse_json --arg sha "$COMMIT_SHA" '. + {statusDetails: {inCommit: {commit: $sha}}}')
  info "Associating with commit: $COMMIT_SHA"
fi

if [ -n "$RELEASE_VERSION" ]; then
  PAYLOAD=$(echo "$PAYLOAD" | parse_json --arg ver "$RELEASE_VERSION" '. + {statusDetails: {inRelease: $ver}}')
  info "Associating with release: $RELEASE_VERSION"
fi

echo ""

# Make the API call
response=$(api_call PUT "/issues/$ISSUE_ID/" "$PAYLOAD")

# Check result
if echo "$response" | grep -q '"status"'; then
  new_status=$(echo "$response" | parse_json -r '.status')
  short_id=$(echo "$response" | parse_json -r '.shortId')

  if [ "$new_status" = "resolved" ]; then
    success "Issue $short_id marked as resolved"

    # Show additional info if available
    if echo "$response" | grep -q '"statusDetails"'; then
      details=$(echo "$response" | parse_json -r '.statusDetails // {}')
      if [ "$details" != "{}" ]; then
        echo ""
        echo "Resolution details:"
        echo "$details" | parse_json '.'
      fi
    fi
  else
    warn "Issue status is now: $new_status (expected: resolved)"
  fi
else
  error_msg=$(echo "$response" | parse_json -r '.detail // "Unknown error"' 2>/dev/null)
  die "Failed to resolve issue: $error_msg"
fi
