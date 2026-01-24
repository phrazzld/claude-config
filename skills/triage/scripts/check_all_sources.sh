#!/bin/bash
# Multi-source triage orchestrator
# Runs all checks in parallel and aggregates results

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Disable errexit for this script - we handle exit codes manually
set +e

# Options
OUTPUT_FORMAT="${1:-summary}"  # summary | detail

# Temporary files for parallel results
TRIAGE_TMPDIR="${TMPDIR:-/tmp}/triage_$$"
mkdir -p "$TRIAGE_TMPDIR"
SENTRY_OUT="$TRIAGE_TMPDIR/sentry"
VERCEL_OUT="$TRIAGE_TMPDIR/vercel"
HEALTH_OUT="$TRIAGE_TMPDIR/health"

# Cleanup on exit
cleanup() {
  rm -rf "$TRIAGE_TMPDIR" 2>/dev/null
}
trap cleanup EXIT

# Header
echo ""
echo "TRIAGE STATUS - $(timestamp)"
echo "================================"

# Run checks in parallel with individual timeouts
timeout 15 "$SCRIPT_DIR/check_sentry.sh" "$OUTPUT_FORMAT" > "$SENTRY_OUT" 2>&1 &
pid_sentry=$!

timeout 15 "$SCRIPT_DIR/check_vercel_logs.sh" "$OUTPUT_FORMAT" > "$VERCEL_OUT" 2>&1 &
pid_vercel=$!

timeout 15 "$SCRIPT_DIR/check_health_endpoints.sh" "$OUTPUT_FORMAT" > "$HEALTH_OUT" 2>&1 &
pid_health=$!

# Wait for all checks
wait $pid_sentry 2>/dev/null; sentry_exit=$?
wait $pid_vercel 2>/dev/null; vercel_exit=$?
wait $pid_health 2>/dev/null; health_exit=$?

# Output results
echo ""
if [ -s "$SENTRY_OUT" ]; then cat "$SENTRY_OUT"; else echo "SENTRY: check timed out"; fi

echo ""
if [ -s "$VERCEL_OUT" ]; then cat "$VERCEL_OUT"; else echo "VERCEL LOGS: check timed out"; fi

echo ""
if [ -s "$HEALTH_OUT" ]; then cat "$HEALTH_OUT"; else echo "HEALTH ENDPOINTS: check timed out"; fi

# Determine overall status and recommendations
echo ""
echo "----------------------------------------"

# Count issues for recommendation
has_critical=false
has_issues=false
top_issue=""

# Check Sentry results for top issue
# Look for actual problems, not "No unresolved issues"
if [ -f "$SENTRY_OUT" ]; then
  # Match "[CRITICAL]" or "N unresolved issues" where N > 0
  if grep -qE "\[CRITICAL\]|[1-9][0-9]* unresolved issues" "$SENTRY_OUT"; then
    has_issues=true
    # Extract top issue ID if present
    top_issue=$(grep -oE "[A-Z]+-[0-9]+" "$SENTRY_OUT" | head -1)
    if grep -q "\[CRITICAL\]" "$SENTRY_OUT"; then
      has_critical=true
    fi
  fi
fi

# Check health endpoint results (match bracketed status indicators)
if grep -qE "\[CRITICAL\]" "$HEALTH_OUT" 2>/dev/null; then
  has_critical=true
  has_issues=true
elif grep -qE "\[WARN\]|SLOW" "$HEALTH_OUT" 2>/dev/null; then
  has_issues=true
fi

# Check Vercel results
if grep -qE "\[CRITICAL\]" "$VERCEL_OUT" 2>/dev/null; then
  has_critical=true
  has_issues=true
elif grep -qE "\[WARN\]" "$VERCEL_OUT" 2>/dev/null; then
  has_issues=true
fi

# Output recommendation
if $has_critical; then
  echo -e "${RED}${BOLD}RECOMMENDATION:${NC}"
  if [ -n "$top_issue" ]; then
    # Extract user count if present
    users=$(grep -oE "[0-9]+ users" "$SENTRY_OUT" | head -1 | grep -oE "[0-9]+")
    echo -e "  ${RED}Investigate $top_issue immediately${NC}"
    [ -n "$users" ] && echo "  $users users affected"
  else
    echo -e "  ${RED}Critical issues detected. Investigate immediately.${NC}"
  fi
  echo ""
  echo "  Next steps:"
  [ -n "$top_issue" ] && echo "    /triage investigate $top_issue"
  echo "    Check Sentry dashboard"
  echo "    Review Vercel logs: vercel logs --since 30m"
elif $has_issues; then
  echo -e "${YELLOW}${BOLD}RECOMMENDATION:${NC}"
  if [ -n "$top_issue" ]; then
    echo "  Review $top_issue when time permits"
    echo ""
    echo "  Next: /triage investigate $top_issue"
  else
    echo "  Minor issues detected. Review when time permits."
  fi
else
  echo -e "${GREEN}${BOLD}All systems nominal.${NC} No action required."
fi

echo ""

# Exit code: 2 for critical, 1 for issues, 0 for clean
if $has_critical; then
  exit 2
elif $has_issues; then
  exit 1
fi
exit 0
