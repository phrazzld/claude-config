#!/bin/bash
# Generate postmortem document from Sentry issue
# Usage: generate_postmortem.sh ISSUE-ID [--output-dir DIR]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# Options
ISSUE_ID=""
OUTPUT_DIR="docs/postmortems"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      echo "Usage: $(basename "$0") ISSUE-ID [OPTIONS]"
      echo ""
      echo "Generate a postmortem document from a Sentry issue."
      echo ""
      echo "Options:"
      echo "  --output-dir DIR   Output directory (default: docs/postmortems)"
      echo "  --dry-run          Print to stdout instead of writing file"
      echo "  --help             Show this help message"
      exit 0
      ;;
    -*)
      die "Unknown option: $1"
      ;;
    *)
      ISSUE_ID="$1"
      shift
      ;;
  esac
done

if [ -z "$ISSUE_ID" ]; then
  die "Issue ID is required. Usage: $(basename "$0") ISSUE-ID"
fi

# Get issue details using sentry-observability script
ISSUE_SCRIPT="$HOME/.claude/skills/sentry-observability/scripts/issue_detail.sh"
if [ ! -x "$ISSUE_SCRIPT" ]; then
  die "issue_detail.sh not found. Install sentry-observability skill."
fi

info "Fetching issue details for $ISSUE_ID..."

issue_json=$("$ISSUE_SCRIPT" "$ISSUE_ID" --json 2>/dev/null)
if [ -z "$issue_json" ] || echo "$issue_json" | grep -q '"detail"'; then
  die "Could not fetch issue details for $ISSUE_ID"
fi

# Extract issue metadata
title=$(echo "$issue_json" | jq -r '.title // "Unknown"' | head -c 60)
short_id=$(echo "$issue_json" | jq -r '.shortId // "UNKNOWN"')
first_seen=$(echo "$issue_json" | jq -r '.firstSeen // "Unknown"')
last_seen=$(echo "$issue_json" | jq -r '.lastSeen // "Unknown"')
event_count=$(echo "$issue_json" | jq -r '.count // 0')
user_count=$(echo "$issue_json" | jq -r '.userCount // 0')
level=$(echo "$issue_json" | jq -r '.level // "error"')
permalink=$(echo "$issue_json" | jq -r '.permalink // ""')

# Determine severity
case "$level" in
  fatal) severity="Critical" ;;
  error) severity="High" ;;
  warning) severity="Medium" ;;
  *) severity="Low" ;;
esac

# Adjust severity based on user impact
if [ "$user_count" -gt 100 ]; then
  severity="Critical"
elif [ "$user_count" -gt 20 ]; then
  [ "$severity" != "Critical" ] && severity="High"
fi

# Format dates
today=$(date "+%Y-%m-%d")
first_seen_date=$(echo "$first_seen" | cut -d'T' -f1)

# Generate filename
filename="${today}-${short_id}.md"
filepath="$OUTPUT_DIR/$filename"

# Generate postmortem content
postmortem_content=$(cat <<EOF
# Postmortem: $title

**Date:** $today
**Severity:** $severity
**Duration:** [Detection to resolution - fill in]
**Author:** [Your name]

## Incident Summary

$title

- **Sentry Issue:** $short_id
- **First Seen:** $first_seen
- **Last Seen:** $last_seen
- **Events:** $event_count
- **Users Affected:** $user_count

[2-3 sentences: Describe the user impact and business consequences]

## Timeline

| Time | Event |
|------|-------|
| $first_seen_date | Incident first detected in Sentry |
| | Investigation started |
| | Root cause identified |
| | Fix deployed |
| $today | Postmortem created |

## Root Cause

[Clear technical explanation of what went wrong]

## 5 Whys Analysis

1. **Why did $title happen?** → Because [immediate cause]
2. **Why was [immediate cause] possible?** → Because [deeper cause]
3. **Why wasn't [deeper cause] prevented?** → Because [process gap]
4. **Why did [process gap] exist?** → Because [systemic issue]
5. **Why wasn't [systemic issue] addressed?** → Because [root cause]

## Contributing Factors

- [ ] Time pressure / rushed deployment
- [ ] Missing or inadequate tests
- [ ] Unclear requirements or documentation
- [ ] Complex code / technical debt
- [ ] Missing code review
- [ ] Insufficient monitoring
- [ ] Configuration management issues
- [ ] Other: [describe]

## Fixes Applied

| Fix | Commit | Lines Changed | Necessary? |
|-----|--------|---------------|------------|
| [Description] | \`abc123\` | +X/-Y | Yes |

## Mitigation Plan

### Preventive Measures

| Action | Owner | Status |
|--------|-------|--------|
| [Add test coverage] | | Pending |
| [Add validation] | | Pending |

### Detection Improvements

| Action | Owner | Status |
|--------|-------|--------|
| [Add alert rule] | | Pending |
| [Improve logging] | | Pending |

### Process Changes

| Action | Owner | Status |
|--------|-------|--------|
| [Update checklist] | | Pending |

## Lessons Learned

### 1. [Key Lesson Title]

[Explanation and how to apply it going forward]

## Related Documents

- [Sentry Issue]($permalink)
- [Fix PR](https://github.com/...)

## Appendix

\`\`\`bash
# Commands used during investigation
# ...
\`\`\`
EOF
)

# Output
if $DRY_RUN; then
  echo "$postmortem_content"
else
  # Ensure output directory exists
  mkdir -p "$OUTPUT_DIR"

  # Write file
  echo "$postmortem_content" > "$filepath"
  success "Created postmortem: $filepath"

  echo ""
  echo "Next steps:"
  echo "  1. Fill in the timeline with specific times"
  echo "  2. Complete the root cause analysis"
  echo "  3. Document the fix and link the PR"
  echo "  4. Resolve the Sentry issue:"
  echo "     ~/.claude/skills/sentry-observability/scripts/resolve_issue.sh $short_id"
fi
