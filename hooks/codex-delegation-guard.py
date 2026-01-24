#!/usr/bin/env python3
"""
Codex delegation guard - enforces delegation of agentic work.

PreToolUse hook that BLOCKS multi-file/substantial edits, forcing
delegation to Codex. Simple edits (<20 lines, single file) pass through.

Session state: /tmp/claude-delegation-{PPID}.json
Bypass: Claude says "I'm self-implementing because [reason]" - allows ONE edit.
"""
import json
import os
import sys
import time
from pathlib import Path

# Thresholds for blocking
MAX_NEW_FILES = 2  # Block on 3rd new file
MAX_DIRECTORIES = 3  # Block on 4th directory
MAX_LINES_SOFT = 50  # Warning threshold
MAX_LINES_HARD = 100  # Block if also multi-file
SIMPLE_EDIT_LINES = 20  # Always allow below this

# Paths that are always allowed (meta-config)
ALWAYS_ALLOW_PATTERNS = [
    "/.claude/",
    ".env",
    "package.json",  # lockfiles, deps
    "pnpm-lock",
    "yarn.lock",
    "package-lock",
]

# Test file patterns (feature pattern detection)
TEST_FILE_PATTERNS = [
    ".test.",
    ".spec.",
    "_test.",
    "_spec.",
    "/tests/",
    "/__tests__/",
]


def get_state_file() -> Path:
    """Get session state file path based on parent PID."""
    ppid = os.getppid()
    return Path(f"/tmp/claude-delegation-{ppid}.json")


def load_state() -> dict:
    """Load session state, creating fresh if missing."""
    state_file = get_state_file()
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "files_touched": [],
        "new_files_created": 0,
        "total_lines_added": 0,
        "directories_touched": [],
        "delegation_acknowledged": False,
        "last_acknowledged_file": None,
        "last_acknowledged_at": None,
    }


def save_state(state: dict) -> None:
    """Save session state."""
    get_state_file().write_text(json.dumps(state, indent=2))


def is_always_allowed(file_path: str) -> bool:
    """Check if path should bypass delegation checks."""
    for pattern in ALWAYS_ALLOW_PATTERNS:
        if pattern in file_path:
            return True
    return False


def is_test_file(file_path: str) -> bool:
    """Check if this is a test file."""
    for pattern in TEST_FILE_PATTERNS:
        if pattern in file_path:
            return True
    return False


def get_directory(file_path: str) -> str:
    """Extract directory from file path."""
    return str(Path(file_path).parent)


def count_lines(tool_input: dict) -> int:
    """Estimate lines being added/changed."""
    new_string = tool_input.get("new_string", "")
    content = tool_input.get("content", "")
    text = new_string or content
    if not text:
        return 0
    return len(text.strip().split("\n"))


def check_acknowledgment_valid(state: dict, file_path: str) -> bool:
    """Check if there's a valid per-edit acknowledgment."""
    ack_file = state.get("last_acknowledged_file")
    ack_time = state.get("last_acknowledged_at")

    if not ack_file or not ack_time:
        return False

    # Must match the file being edited
    if ack_file != file_path:
        return False

    # Must be within 60 seconds
    try:
        elapsed = time.time() - float(ack_time)
        if elapsed > 60:
            return False
    except (ValueError, TypeError):
        return False

    return True


def consume_acknowledgment(state: dict) -> None:
    """Clear acknowledgment after use (one-time bypass)."""
    state["last_acknowledged_file"] = None
    state["last_acknowledged_at"] = None
    save_state(state)


def format_codex_command(description: str = "[describe task]") -> str:
    """Format the suggested codex command."""
    return f'''codex exec --full-auto "{description}. Follow pattern in [ref]." \\
    --output-last-message /tmp/codex-out.md 2>/dev/null'''


def block(reason: str) -> None:
    """Block the edit with structured output."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def warn(message: str) -> None:
    """Warn but allow the edit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "message": message
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    if tool_name not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Always allow meta-config paths
    if is_always_allowed(file_path):
        sys.exit(0)

    state = load_state()
    lines = count_lines(tool_input)
    directory = get_directory(file_path)
    is_new_file = tool_name == "Write"
    is_test = is_test_file(file_path)

    # Check for valid per-edit acknowledgment
    if check_acknowledgment_valid(state, file_path):
        consume_acknowledgment(state)
        sys.exit(0)  # Allow this one edit

    # Update state for this edit
    if file_path not in state["files_touched"]:
        state["files_touched"].append(file_path)
    if directory not in state["directories_touched"]:
        state["directories_touched"].append(directory)
    if is_new_file:
        state["new_files_created"] += 1
    state["total_lines_added"] += lines

    # Save updated state before checking thresholds
    save_state(state)

    # Calculate current metrics
    num_files = len(state["files_touched"])
    num_dirs = len(state["directories_touched"])
    total_lines = state["total_lines_added"]
    new_files = state["new_files_created"]

    # Simple edit check - always allow
    if num_files == 1 and lines <= SIMPLE_EDIT_LINES and not is_new_file:
        sys.exit(0)

    # Build session summary
    session_summary = f"Session: {num_files} files, {total_lines} lines, {num_dirs} directories"
    if new_files > 0:
        session_summary += f", {new_files} new files"

    # Blocking checks
    block_reasons = []

    # Check: Creating too many new files
    if new_files >= 3:
        block_reasons.append(f"Creating {new_files} new files (threshold: 2)")

    # Check: Too many directories
    if num_dirs >= 4:
        block_reasons.append(f"Editing {num_dirs} directories (threshold: 3)")

    # Check: Feature pattern (implementation + test)
    non_test_files = [f for f in state["files_touched"] if not is_test_file(f)]
    test_files = [f for f in state["files_touched"] if is_test_file(f)]
    if non_test_files and test_files:
        block_reasons.append("Feature pattern: implementation + test files")

    # Check: Substantial multi-file work
    if total_lines >= MAX_LINES_HARD and num_files >= 3:
        block_reasons.append(f"{total_lines} lines across {num_files} files")

    if block_reasons:
        reasons_str = "\n- ".join(block_reasons)
        block(
            f"BLOCKED: Agentic work detected - delegate to Codex\n\n"
            f"{session_summary}\n\n"
            f"Reasons:\n- {reasons_str}\n\n"
            f"Delegate:\n  {format_codex_command()}\n\n"
            f"Then: git diff --stat && pnpm test\n\n"
            f"To self-implement: Say \"I'm self-implementing [file] because [reason]\""
        )

    # Soft warning for approaching thresholds
    warnings = []
    if total_lines >= MAX_LINES_SOFT:
        warnings.append(f"{total_lines} lines (hard limit: {MAX_LINES_HARD})")
    if num_files >= 2:
        warnings.append(f"{num_files} files touched")
    if new_files >= 2:
        warnings.append(f"{new_files} new files (limit: 2)")

    if warnings:
        warn(
            f"⚠️  Approaching delegation threshold\n\n"
            f"{session_summary}\n\n"
            f"Consider delegating:\n  {format_codex_command()}"
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
