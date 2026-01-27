#!/bin/bash
# Check GitHub CI/CD status for current repo
# Usage: check_github_ci.sh [--branch BRANCH]

set -euo pipefail

BRANCH="${1:-}"
if [[ "$BRANCH" == "--branch" ]]; then
  BRANCH="${2:-main}"
else
  # Try to detect default branch
  BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || echo "main")
fi

echo "GITHUB CI/CD STATUS"
echo "==================="
echo ""

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
  echo "⚠ GitHub CLI (gh) not installed"
  exit 1
fi

# Check if we're in a git repo with GitHub remote
if ! gh repo view &> /dev/null; then
  echo "⚠ Not in a GitHub repository"
  exit 1
fi

REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
echo "Repository: $REPO"
echo "Default branch: $BRANCH"
echo ""

# Failed runs on default branch (blocking deploys)
echo "## Default Branch ($BRANCH) Failures"
MAIN_FAILURES=$(gh run list --branch "$BRANCH" --status failure --limit 5 --json databaseId,name,conclusion,createdAt,headBranch 2>/dev/null || echo "[]")

if [[ "$MAIN_FAILURES" == "[]" ]] || [[ -z "$MAIN_FAILURES" ]]; then
  echo "✓ No failures on $BRANCH"
else
  echo "✗ Failures found:"
  echo "$MAIN_FAILURES" | jq -r '.[] | "  - [\(.databaseId)] \(.name) - \(.createdAt)"'
  echo ""
  echo "[P1] Main branch CI failing - blocks deploys"
fi
echo ""

# All recent failures
echo "## Recent Failures (all branches)"
ALL_FAILURES=$(gh run list --status failure --limit 10 --json databaseId,name,headBranch,createdAt 2>/dev/null || echo "[]")

if [[ "$ALL_FAILURES" == "[]" ]] || [[ -z "$ALL_FAILURES" ]]; then
  echo "✓ No recent failures"
else
  FAILURE_COUNT=$(echo "$ALL_FAILURES" | jq 'length')
  echo "✗ $FAILURE_COUNT failed runs:"
  echo "$ALL_FAILURES" | jq -r '.[] | "  - [\(.databaseId)] \(.name) on \(.headBranch) - \(.createdAt)"'
fi
echo ""

# In-progress runs (check for stuck)
echo "## In Progress"
IN_PROGRESS=$(gh run list --status in_progress --limit 5 --json databaseId,name,headBranch,createdAt 2>/dev/null || echo "[]")

if [[ "$IN_PROGRESS" == "[]" ]] || [[ -z "$IN_PROGRESS" ]]; then
  echo "✓ No runs in progress"
else
  echo "⏳ Running:"
  echo "$IN_PROGRESS" | jq -r '.[] | "  - [\(.databaseId)] \(.name) on \(.headBranch) - started \(.createdAt)"'
fi
echo ""

# Summary
echo "## Summary"
MAIN_FAIL_COUNT=$(echo "$MAIN_FAILURES" | jq 'if type == "array" then length else 0 end')
ALL_FAIL_COUNT=$(echo "$ALL_FAILURES" | jq 'if type == "array" then length else 0 end')

if [[ "$MAIN_FAIL_COUNT" -gt 0 ]]; then
  echo "[P1] Fix main branch CI immediately"
  FIRST_FAIL=$(echo "$MAIN_FAILURES" | jq -r '.[0].databaseId')
  echo "     Run: /triage investigate-ci $FIRST_FAIL"
elif [[ "$ALL_FAIL_COUNT" -gt 0 ]]; then
  echo "[P2] $ALL_FAIL_COUNT feature branch failures (may block PRs)"
else
  echo "✓ All CI checks passing"
fi
