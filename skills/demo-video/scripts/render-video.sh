#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <composition-name> <output.mp4> [-- extra remotion args]"
}

if [[ "${1:-}" == "" || "${2:-}" == "" ]]; then
  usage
  exit 1
fi

COMP="$1"
OUT="$2"
shift 2

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx not found. Install Node.js first."
  exit 1
fi

echo "Rendering composition '${COMP}' -> ${OUT}"
if npx remotion render "${COMP}" "${OUT}" "$@"; then
  echo "Render complete: ${OUT}"
  exit 0
fi

echo "Render failed. Common fixes:"
echo "- Verify composition name: npx remotion compositions"
echo "- Install deps: npm install / pnpm install"
echo "- Ensure Remotion is configured in this project"
exit 1
