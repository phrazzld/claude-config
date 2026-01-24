#!/bin/bash
# Check health endpoints for PRODUCTION services only
# Never checks localhost - that's noise, not signal

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"
set +e  # Don't exit on errors

# Options
OUTPUT_FORMAT="${1:-summary}"  # summary | json | detail
TIMEOUT="${TRIAGE_HEALTH_TIMEOUT:-10}"  # seconds

# Determine URLs to check (production only!)
URLS=()

# 1. Explicit HEALTH_ENDPOINTS env var (comma-separated)
if [ -n "${HEALTH_ENDPOINTS:-}" ]; then
  IFS=',' read -ra URLS <<< "$HEALTH_ENDPOINTS"
fi

# 2. Check .triage.json in project root
if [ ${#URLS[@]} -eq 0 ] && [ -f ".triage.json" ]; then
  if has_command jq; then
    url=$(jq -r '.healthEndpoint // empty' .triage.json 2>/dev/null)
    [ -n "$url" ] && URLS+=("$url")
  fi
fi

# 3. Check for Vercel production domain via vercel CLI
if [ ${#URLS[@]} -eq 0 ] && [ -f ".vercel/project.json" ]; then
  if has_command jq; then
    # Try to get production URL from Vercel project
    project_name=$(jq -r '.projectId // empty' .vercel/project.json 2>/dev/null)
    if [ -n "$project_name" ]; then
      # Common pattern: project-name.vercel.app or custom domain
      # Check if there's a domains file or inspect vercel.json
      if [ -f "vercel.json" ]; then
        domain=$(jq -r '.alias[0] // empty' vercel.json 2>/dev/null)
        [ -n "$domain" ] && URLS+=("https://$domain")
      fi
    fi
  fi
fi

# 4. Check package.json for homepage
if [ ${#URLS[@]} -eq 0 ] && [ -f "package.json" ]; then
  if has_command jq; then
    homepage=$(jq -r '.homepage // empty' package.json 2>/dev/null)
    [ -n "$homepage" ] && URLS+=("$homepage")
  fi
fi

# 5. Known project mappings (fallback for well-known projects)
if [ ${#URLS[@]} -eq 0 ]; then
  project_name=$(basename "$PWD")
  case "$project_name" in
    volume|volume-fitness)
      URLS+=("https://volume.fitness")
      ;;
    # Add other known projects here
  esac
fi

# If no production URLs found, skip gracefully (not an error!)
if [ ${#URLS[@]} -eq 0 ]; then
  echo "HEALTH ENDPOINTS"
  echo "  [SKIP] No production URL configured"
  echo "  Set HEALTH_ENDPOINTS env var or add .triage.json with healthEndpoint"
  exit 0
fi

# Results storage
declare -a results
all_ok=true
has_critical=false

# Check each endpoint
for url in "${URLS[@]}"; do
  # Normalize URL (ensure /api/health)
  if [[ ! "$url" =~ /api/health$ ]]; then
    url="${url%/}/api/health"
  fi

  # Extract domain for display
  domain=$(echo "$url" | sed -E 's|https?://||' | cut -d'/' -f1)

  # Make request with timing (follow redirects!)
  start_time=$(date +%s%N)
  response=$(curl -sL -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" "$url" 2>/dev/null || echo "000")
  end_time=$(date +%s%N)

  # Calculate response time in ms
  response_time=$(( (end_time - start_time) / 1000000 ))

  # Determine status
  if [ "$response" = "200" ]; then
    status="ok"
    if [ "$response_time" -gt 2000 ]; then
      status="slow"
      all_ok=false
    fi
  elif [ "$response" = "000" ]; then
    status="timeout"
    all_ok=false
    has_critical=true
  else
    status="error"
    all_ok=false
    has_critical=true
  fi

  results+=("$domain|$response|$response_time|$status")
done

# Output results
case "$OUTPUT_FORMAT" in
  json)
    echo "["
    first=true
    for result in "${results[@]}"; do
      IFS='|' read -r domain code time status <<< "$result"
      $first || echo ","
      first=false
      cat <<EOF
  {
    "domain": "$domain",
    "status_code": $code,
    "response_time_ms": $time,
    "status": "$status"
  }
EOF
    done
    echo "]"
    ;;
  *)
    # summary and detail (same output)
    echo "HEALTH ENDPOINTS"
    for result in "${results[@]}"; do
      IFS='|' read -r domain code time status <<< "$result"
      case "$status" in
        ok)
          status_ok "$domain ($code, ${time}ms)"
          ;;
        slow)
          status_warn "$domain ($code, ${time}ms - SLOW)"
          ;;
        timeout)
          status_critical "$domain (timeout after ${TIMEOUT}s)"
          ;;
        error)
          status_critical "$domain (HTTP $code)"
          ;;
      esac
    done
    ;;
esac

# Exit code reflects health
if $has_critical; then
  exit 2
elif ! $all_ok; then
  exit 1
fi
exit 0
