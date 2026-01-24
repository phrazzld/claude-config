#!/usr/bin/env python3
"""
Codex session initialization - resets delegation state.

SessionStart hook that clears previous session state and
reminds that delegation is enforced.
"""
import json
import os
import sys
from pathlib import Path


def get_state_file() -> Path:
    """Get session state file path based on parent PID."""
    ppid = os.getppid()
    return Path(f"/tmp/claude-delegation-{ppid}.json")


def main():
    # Initialize fresh state
    state = {
        "files_touched": [],
        "new_files_created": 0,
        "total_lines_added": 0,
        "directories_touched": [],
        "delegation_acknowledged": False,
        "last_acknowledged_file": None,
        "last_acknowledged_at": None,
    }

    state_file = get_state_file()
    state_file.write_text(json.dumps(state, indent=2))

    print(
        "[codex] Delegation enforcement active. "
        "Multi-file/substantial edits → Codex."
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
