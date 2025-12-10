#!/bin/bash
# Calculate priority scores for Sentry issues using /triage algorithm

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Default options
ENV_FILTER="production"
LIMIT=20
PROJECT_ARG=""
ORG_ARG=""
OUTPUT_JSON=false

# Scoring weights (from /triage command)
WEIGHT_EVENTS=1
WEIGHT_USERS=5
WEIGHT_SEVERITY=3
WEIGHT_RECENCY=2
WEIGHT_ENV=4

HELP_TEXT="Usage: $(basename "$0") [OPTIONS]

Calculate priority scores for Sentry issues using the /triage algorithm.

Scoring: Events(${WEIGHT_EVENTS}x) + Users(${WEIGHT_USERS}x) + Severity(${WEIGHT_SEVERITY}x) + Recency(${WEIGHT_RECENCY}x) + Env(${WEIGHT_ENV}x)

Options:
  --env ENV        Environment filter (default: production)
  --limit N        Maximum issues to score (default: 20)
  --project SLUG   Override auto-detected project
  --org SLUG       Override organization
  --json           Output JSON with scores
  --help           Show this help message

Examples:
  $(basename "$0")                    # Score production issues
  $(basename "$0") --limit 50 --json  # Score 50 issues, output JSON"

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
require_auth

# Resolve org and project
ORG=$(resolve_org "$ORG_ARG")
PROJECT=$(resolve_project "$PROJECT_ARG")

info "Calculating priority scores for $ORG/$PROJECT (env: $ENV_FILTER)"
echo ""

# Fetch issues
response=$(api_call GET "/projects/$ORG/$PROJECT/issues/?query=is:unresolved+environment:$ENV_FILTER&limit=$LIMIT")

if ! echo "$response" | grep -q '"id"'; then
  if echo "$response" | grep -q '"detail"'; then
    die "API error: $(echo "$response" | parse_json -r '.detail')"
  fi
  echo "No issues found."
  exit 0
fi

# Calculate scores using jq
scored_issues=$(echo "$response" | parse_json --argjson we "$WEIGHT_EVENTS" \
  --argjson wu "$WEIGHT_USERS" \
  --argjson ws "$WEIGHT_SEVERITY" \
  --argjson wr "$WEIGHT_RECENCY" \
  --argjson wenv "$WEIGHT_ENV" \
  --arg env "$ENV_FILTER" '
  def severity_mult:
    if . == "fatal" then 10
    elif . == "error" then 5
    elif . == "warning" then 2
    else 1
    end;

  def recency_mult:
    (now - (. | fromdateiso8601)) / 3600 |  # hours ago
    if . < 1 then 10
    elif . < 6 then 5
    elif . < 24 then 2
    else 1
    end;

  def env_mult:
    if $env == "production" then 10
    elif $env == "preview" then 2
    else 1
    end;

  [.[] | {
    id: .shortId,
    title: .title,
    events: .count,
    users: .userCount,
    level: .level,
    firstSeen: .firstSeen,
    lastSeen: .lastSeen,
    permalink: .permalink,
    score: (
      ((.count // 0) * $we) +
      ((.userCount // 0) * $wu) +
      ((.level // "error") | severity_mult) * $ws +
      ((.firstSeen // "2020-01-01T00:00:00Z") | recency_mult) * $wr +
      (env_mult * $wenv)
    )
  }] | sort_by(-.score)
')

if [ "$OUTPUT_JSON" = true ]; then
  echo "$scored_issues"
else
  # Format as table
  echo "Priority-Scored Issues (highest first)"
  echo "======================================="
  echo ""
  printf "${BLUE}%-8s %-12s %-40s %8s %8s %8s${NC}\n" "RANK" "ID" "TITLE" "SCORE" "EVENTS" "USERS"
  printf "%-8s %-12s %-40s %8s %8s %8s\n" "--------" "------------" "----------------------------------------" "--------" "--------" "--------"

  rank=1
  echo "$scored_issues" | parse_json -r '.[] | [.id, .title, .score, .events, .users] | @tsv' | \
  while IFS=$'\t' read -r id title score events users; do
    title_truncated=$(truncate "$title" 40)
    printf "%-8s %-12s %-40s %8.0f %8s %8s\n" "#$rank" "$id" "$title_truncated" "$score" "$events" "$users"
    ((rank++))
  done

  echo ""
  echo "Scoring: Events(${WEIGHT_EVENTS}x) + Users(${WEIGHT_USERS}x) + Severity(${WEIGHT_SEVERITY}x) + Recency(${WEIGHT_RECENCY}x) + Env(${WEIGHT_ENV}x)"
  echo ""
  echo "To get details on the top issue:"
  top_id=$(echo "$scored_issues" | parse_json -r '.[0].id // empty')
  if [ -n "$top_id" ]; then
    echo "  $SCRIPT_DIR/issue_detail.sh $top_id"
  fi
fi
