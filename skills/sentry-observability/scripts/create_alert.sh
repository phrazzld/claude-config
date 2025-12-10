#!/bin/bash
# Create Sentry alert rules via API

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Default options
ALERT_NAME=""
ALERT_TYPE="issue"
THRESHOLD=100
FREQUENCY="1h"
PROJECT_ARG=""
ORG_ARG=""
DRY_RUN=false

HELP_TEXT="Usage: $(basename "$0") [OPTIONS]

Create Sentry alert rules via the API.

Options:
  --name NAME      Alert rule name (required)
  --type TYPE      Alert type: issue, threshold (default: issue)
  --threshold N    Trigger threshold for threshold alerts (default: 100)
  --frequency F    Check frequency: 5m, 15m, 1h, 24h (default: 1h)
  --project SLUG   Override auto-detected project
  --org SLUG       Override organization
  --dry-run        Show what would be created without creating
  --help           Show this help message

Alert Types:
  issue      - Alert on new issue types (first seen)
  threshold  - Alert when error count exceeds threshold

Examples:
  $(basename "$0") --name 'New Errors'
  $(basename "$0") --name 'High Error Rate' --type threshold --threshold 50
  $(basename "$0") --name 'Test Alert' --dry-run"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --name)
      ALERT_NAME="$2"
      shift 2
      ;;
    --type)
      ALERT_TYPE="$2"
      shift 2
      ;;
    --threshold)
      THRESHOLD="$2"
      shift 2
      ;;
    --frequency)
      FREQUENCY="$2"
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
    --dry-run)
      DRY_RUN=true
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

# Validate
if [ -z "$ALERT_NAME" ]; then
  die "Alert name is required. Use --name 'Alert Name'"
fi

require_auth

# Resolve org and project
ORG=$(resolve_org "$ORG_ARG")
PROJECT=$(resolve_project "$PROJECT_ARG")

# Convert frequency to minutes
case $FREQUENCY in
  5m) FREQ_MINS=5 ;;
  15m) FREQ_MINS=15 ;;
  1h) FREQ_MINS=60 ;;
  24h) FREQ_MINS=1440 ;;
  *) die "Invalid frequency: $FREQUENCY. Use 5m, 15m, 1h, or 24h" ;;
esac

# Build alert payload based on type
case $ALERT_TYPE in
  issue)
    # First seen event alert
    PAYLOAD=$(cat <<EOF
{
  "name": "$ALERT_NAME",
  "actionMatch": "any",
  "filterMatch": "all",
  "frequency": $FREQ_MINS,
  "conditions": [
    {"id": "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition"}
  ],
  "actions": [
    {
      "id": "sentry.mail.actions.NotifyEmailAction",
      "targetType": "IssueOwners",
      "fallthroughType": "ActiveMembers"
    }
  ],
  "filters": []
}
EOF
)
    ;;

  threshold)
    # Error count threshold alert
    PAYLOAD=$(cat <<EOF
{
  "name": "$ALERT_NAME",
  "actionMatch": "any",
  "filterMatch": "all",
  "frequency": $FREQ_MINS,
  "conditions": [
    {
      "id": "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
      "value": $THRESHOLD,
      "comparisonType": "count",
      "interval": "1h"
    }
  ],
  "actions": [
    {
      "id": "sentry.mail.actions.NotifyEmailAction",
      "targetType": "IssueOwners",
      "fallthroughType": "ActiveMembers"
    }
  ],
  "filters": []
}
EOF
)
    ;;

  *)
    die "Unknown alert type: $ALERT_TYPE. Use 'issue' or 'threshold'"
    ;;
esac

info "Creating alert: $ALERT_NAME"
info "Type: $ALERT_TYPE"
info "Project: $ORG/$PROJECT"
info "Frequency: $FREQUENCY"
if [ "$ALERT_TYPE" = "threshold" ]; then
  info "Threshold: $THRESHOLD events"
fi
echo ""

if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}[DRY RUN]${NC} Would create alert with payload:"
  echo "$PAYLOAD" | parse_json '.'
  exit 0
fi

# Create the alert
response=$(api_call POST "/projects/$ORG/$PROJECT/rules/" "$PAYLOAD")

# Check result
if echo "$response" | grep -q '"id"'; then
  rule_id=$(echo "$response" | parse_json -r '.id')
  rule_name=$(echo "$response" | parse_json -r '.name')
  success "Created alert: $rule_name (ID: $rule_id)"
  echo ""
  echo "View in Sentry:"
  echo "  https://sentry.io/settings/$ORG/projects/$PROJECT/alerts/rules/$rule_id/"
else
  error_msg=$(echo "$response" | parse_json -r '.detail // .message // "Unknown error"' 2>/dev/null)
  die "Failed to create alert: $error_msg"
fi
