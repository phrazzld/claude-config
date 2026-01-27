#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/.claude"
SKILLS_DIR="${ROOT}/skills"

is_installed() {
  ls "${SKILLS_DIR}" 2>/dev/null | grep -Eqi 'remotion'
}

if is_installed; then
  echo "Remotion skills already installed."
  exit 0
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx not found. Install Node.js first."
  exit 1
fi

echo "Installing Remotion skills via npx..."
if ! npx skills add remotion-dev/skills; then
  echo "Error: install command failed."
  exit 1
fi

if is_installed; then
  echo "Remotion skills installed successfully."
else
  echo "Error: Remotion skills not detected after install."
  exit 1
fi
