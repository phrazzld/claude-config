#!/usr/bin/env python3
"""qmd-auto-index.py - PostToolUse hook

Runs 'qmd update' (incremental, fast) when journal files are written/edited.
Non-blocking — fires and forgets so it never delays Claude's response.
"""
import json
import os
import subprocess
import sys


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    journal_root = os.path.expanduser("~/Documents/daybook/journal")

    if not file_path.startswith(journal_root):
        sys.exit(0)

    qmd_bin = os.path.expanduser("~/.bun/bin/qmd")
    if os.path.exists(qmd_bin):
        subprocess.Popen(
            [qmd_bin, "update"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )


if __name__ == "__main__":
    main()
