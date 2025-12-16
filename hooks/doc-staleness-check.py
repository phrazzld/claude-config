#!/usr/bin/env python3
"""
Claude Code PostToolUse hook to detect stale documentation.

After Edit/Write/MultiEdit, checks if the edited file's directory (and ancestors)
have documentation that is older than the edited file. Percolates up through
all ancestor directories to the repo root.

Non-blocking: reminds Claude about stale docs without interrupting workflow.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

DOC_FILES = ["README.md", "DOCS.md", "README.rst", "index.md"]


def find_repo_root(start_path: Path) -> Path:
    """Find git repo root by looking for .git directory."""
    current = start_path
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path  # Fallback to start if no .git found


def get_doc_in_dir(directory: Path) -> Path | None:
    """Find documentation file in directory."""
    for doc_name in DOC_FILES:
        doc_path = directory / doc_name
        if doc_path.exists():
            return doc_path
    return None


def format_age(mtime: float) -> str:
    """Format file age as human-readable string."""
    age = datetime.now() - datetime.fromtimestamp(mtime)
    days = age.days
    if days == 0:
        hours = age.seconds // 3600
        if hours == 0:
            return "just now"
        return f"{hours}h ago"
    elif days == 1:
        return "1 day ago"
    elif days < 30:
        return f"{days} days ago"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"


def check_stale_docs(file_path: str) -> list[tuple[Path, float]]:
    """
    Check for stale docs in file's directory and all ancestors up to repo root.
    Returns list of (doc_path, doc_mtime) for stale docs.
    """
    edited_path = Path(file_path).resolve()

    if not edited_path.exists():
        return []

    edited_mtime = edited_path.stat().st_mtime
    repo_root = find_repo_root(edited_path.parent)

    stale_docs = []
    current_dir = edited_path.parent

    # Walk up from edited file's directory to repo root
    while current_dir >= repo_root:
        doc_path = get_doc_in_dir(current_dir)
        if doc_path:
            doc_mtime = doc_path.stat().st_mtime
            if doc_mtime < edited_mtime:
                stale_docs.append((doc_path, doc_mtime))

        if current_dir == repo_root:
            break
        current_dir = current_dir.parent

    return stale_docs


def main():
    try:
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_output = input_data.get("tool_output", {})

        response = {
            "continue": True,
            "suppressOutput": True
        }

        # Only check for file modification operations
        if tool_name not in ["Edit", "Write", "MultiEdit", "NotebookEdit"]:
            print(json.dumps(response))
            sys.exit(0)

        # Skip if operation failed
        if "error" in tool_output:
            print(json.dumps(response))
            sys.exit(0)

        # Get file path from tool input
        file_path = tool_input.get("file_path", "")
        if not file_path:
            print(json.dumps(response))
            sys.exit(0)

        # Skip if editing documentation itself
        if any(file_path.endswith(doc) for doc in DOC_FILES):
            print(json.dumps(response))
            sys.exit(0)

        # Check for stale docs
        stale_docs = check_stale_docs(file_path)

        if stale_docs:
            edited_name = Path(file_path).name

            # Build message
            lines = [f"Docs may be stale after editing {edited_name}:"]
            for doc_path, doc_mtime in stale_docs:
                age = format_age(doc_mtime)
                # Show relative path from cwd or absolute if outside
                try:
                    rel_path = doc_path.relative_to(Path.cwd())
                except ValueError:
                    rel_path = doc_path
                lines.append(f"  - {rel_path} ({age})")

            lines.append("")
            lines.append("Consider updating documentation to reflect your changes.")

            response["systemMessage"] = "\n".join(lines)

        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        error_response = {
            "continue": True,
            "systemMessage": f"Doc staleness hook error (non-blocking): {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)


if __name__ == "__main__":
    main()
