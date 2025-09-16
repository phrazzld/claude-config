#!/usr/bin/env python3
"""
Claude Code PostToolUse hook to remind about atomic commits when uncommitted changes exist.

This hook runs after Edit/Write/MultiEdit operations to check git status and remind
about the Carmack Rule: "A task without a commit is a task not done."
"""

import json
import sys
import subprocess
import os

def check_git_status():
    """Check if there are uncommitted changes in the git repository."""
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=1
        )

        if result.returncode != 0:
            return False, []

        # Get git status
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            capture_output=True,
            text=True,
            timeout=2
        )

        if result.returncode == 0 and result.stdout.strip():
            # Parse changed files
            changed_files = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Extract filename (skip first 3 chars which are status codes)
                    filename = line[3:].strip()
                    changed_files.append(filename)
            return True, changed_files

        return False, []

    except subprocess.TimeoutExpired:
        return False, []
    except Exception:
        return False, []

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_output = input_data.get("tool_output", {})

        # Initialize response
        response = {
            "continue": True,  # Don't block the tool output
            "suppressOutput": True  # Don't show raw output in transcript
        }

        # Check for file modification operations
        if tool_name in ["Edit", "Write", "MultiEdit", "NotebookEdit"]:
            # Skip if the operation failed
            if "error" in tool_output:
                print(json.dumps(response))
                sys.exit(0)

            # Check git status for uncommitted changes
            has_changes, changed_files = check_git_status()

            if has_changes:
                # Build the reminder message
                file_count = len(changed_files)
                files_preview = changed_files[:3]  # Show first 3 files

                message = (
                    "💾 Commit Reminder: You have uncommitted changes!\n\n"
                    f"Modified files ({file_count} total):\n"
                )

                for file in files_preview:
                    message += f"  • {file}\n"

                if file_count > 3:
                    message += f"  • ... and {file_count - 3} more\n"

                message += (
                    "\nThe Carmack Rule: 'A task without a commit is a task not done.'\n\n"
                    "Consider:\n"
                    "  git add -p      # Stage changes interactively\n"
                    "  git commit -m \"type: description\"\n\n"
                    "Atomic commits = Clean history = Happy debugging"
                )

                response["systemMessage"] = message

        # Output the response
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        # On error, allow the tool to continue but log the issue
        error_response = {
            "continue": True,
            "systemMessage": f"Hook error (non-blocking): {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)

if __name__ == "__main__":
    main()