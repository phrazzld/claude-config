#!/usr/bin/env python3
"""
Auto-codify hook - runs at session end to suggest codification.

Scans recent work for patterns worth preserving. Outputs suggestions
that Claude can act on in next session or ignores if nothing notable.
"""

import json
import subprocess
import sys
from pathlib import Path

def get_recent_changes():
    """Get files changed in recent commits."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~5", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        return []

def count_pattern_occurrences(pattern: str, files: list[str]) -> int:
    """Count how many times a pattern appears across files."""
    count = 0
    for f in files:
        try:
            result = subprocess.run(
                ["rg", "-c", pattern, f],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip():
                count += int(result.stdout.strip())
        except:
            pass
    return count

def main():
    # Get context from stdin (Claude Code hook protocol)
    try:
        context = json.load(sys.stdin)
    except:
        context = {}

    # Check for recent changes
    changed_files = get_recent_changes()

    if not changed_files:
        # No recent work, nothing to codify
        sys.exit(0)

    # Look for potential patterns (simple heuristics)
    suggestions = []

    # Check for repeated error handling patterns
    error_count = count_pattern_occurrences(r"try\s*{|catch\s*\(|\.catch\(", changed_files)
    if error_count >= 5:
        suggestions.append("Multiple error handling blocks - consider extracting to utility")

    # Check for repeated type definitions
    type_count = count_pattern_occurrences(r"type\s+\w+\s*=|interface\s+\w+", changed_files)
    if type_count >= 5:
        suggestions.append("Multiple type definitions added - consider consolidating")

    # If we found patterns worth noting, add to staging
    if suggestions:
        staging_note = f"\n<!-- Auto-codify suggestions from session:\n"
        for s in suggestions:
            staging_note += f"- {s}\n"
        staging_note += "-->\n"

        # Could append to CLAUDE.md staging section here
        # For now, just output as info
        print(json.dumps({
            "result": "continue",
            "message": f"Codification candidates: {len(suggestions)} patterns detected"
        }))
    else:
        print(json.dumps({"result": "continue"}))

if __name__ == "__main__":
    main()
