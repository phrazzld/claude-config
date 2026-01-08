#!/usr/bin/env python3
"""
Destructive command guard for Claude Code.

Blocks dangerous git and filesystem commands that can lose uncommitted work.
PreToolUse hook - runs before Bash commands execute.

Exit 0 + JSON with permissionDecision: "deny" = block the command
Exit 0 + no output = allow the command
"""
import json
import re
import sys

# Patterns that indicate destructive commands
DESTRUCTIVE = [
    # (substring_to_match, reason)
    ("git checkout -- ", "Discards uncommitted changes permanently. Use 'git stash' first."),
    ("git reset --hard", "Destroys all uncommitted work. Use 'git stash' first."),
    ("git clean -f", "Deletes untracked files permanently. Use 'git clean -n' to preview first."),
    ("git push --force", "Overwrites remote history. Use '--force-with-lease' instead."),
    ("git push -f", "Overwrites remote history. Use '--force-with-lease' instead."),
    ("git branch -D", "Force-deletes branch without merge check. Use '-d' for safety."),
    ("git stash drop", "Permanently deletes stashed changes."),
    ("git stash clear", "Permanently deletes ALL stashed changes."),
    ("git restore ", "Can discard uncommitted changes. Be careful."),
]

# Patterns that override DESTRUCTIVE (checked first)
SAFE = [
    "git checkout -b",         # new branch
    "git checkout --orphan",   # orphan branch
    "git restore --staged",    # unstaging is safe
    "git restore -S",          # unstaging short form
    "git clean -n",            # dry run
    "git clean --dry-run",     # dry run long form
    "--force-with-lease",      # safe force push
    "--force-if-includes",     # safe force push variant
]

# Build artifact directories safe to rm -rf
BUILD_DIRS = [
    "node_modules", ".next", "dist", "build", "__pycache__",
    ".cache", "target", ".turbo", ".parcel-cache", "coverage",
    ".nyc_output", ".pytest_cache", ".mypy_cache", ".ruff_cache",
]

# Temp directories always safe
TEMP_DIRS = ["/tmp/", "/var/tmp/", "$TMPDIR", "${TMPDIR"]


def has_rm_rf_flags(cmd: str) -> bool:
    """Check if rm command has both recursive and force flags."""
    if "rm " not in cmd:
        return False

    # Match flag groups like -rf, -fr, -Rf, -fR, -rfi, etc.
    # Also match separate flags: -r -f, -R -f, etc.
    flag_pattern = r"-[a-zA-Z]*[rR][a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*[rR]"
    if re.search(flag_pattern, cmd):
        return True

    # Check for separate -r/-R and -f flags
    has_recursive = bool(re.search(r"-[a-zA-Z]*[rR]", cmd))
    has_force = bool(re.search(r"-[a-zA-Z]*f", cmd)) or "--force" in cmd
    return has_recursive and has_force


def is_safe_rm_rf(cmd: str) -> bool:
    """Check if rm -rf targets a safe directory."""
    if not has_rm_rf_flags(cmd):
        return True  # not rm -rf, allow

    # Check temp directories
    for temp in TEMP_DIRS:
        if temp in cmd:
            return True

    # Check build artifact directories (anywhere in path)
    for build_dir in BUILD_DIRS:
        # Match /node_modules, ./node_modules, path/node_modules
        if f"/{build_dir}" in cmd or f" {build_dir}" in cmd or f"./{build_dir}" in cmd:
            return True

    return False


def check_command(cmd: str) -> tuple[bool, str]:
    """
    Check if command should be blocked.
    Returns (should_block, reason).
    """
    if not cmd:
        return False, ""

    # Check safe patterns first (allowlist)
    for safe in SAFE:
        if safe in cmd:
            return False, ""

    # Check destructive git patterns
    for pattern, reason in DESTRUCTIVE:
        if pattern in cmd:
            return True, reason

    # Special handling for rm -rf
    if has_rm_rf_flags(cmd) and not is_safe_rm_rf(cmd):
        return True, "rm -rf on non-temp/non-build path. Run manually if needed."

    return False, ""


def deny(cmd: str, reason: str) -> None:
    """Output deny decision and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"BLOCKED: {reason}\n\n"
                f"Command: {cmd}\n\n"
                f"Run this yourself if truly needed."
            )
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # can't parse, allow

    if data.get("tool_name") != "Bash":
        sys.exit(0)  # not a Bash command, allow

    tool_input = data.get("tool_input") or {}
    cmd = tool_input.get("command", "")

    if not isinstance(cmd, str) or not cmd:
        sys.exit(0)  # no command, allow

    should_block, reason = check_command(cmd)

    if should_block:
        deny(cmd, reason)

    # Allow
    sys.exit(0)


if __name__ == "__main__":
    main()
