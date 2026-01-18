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
import subprocess
import sys

# Patterns that indicate destructive commands
DESTRUCTIVE = [
    # (substring_to_match, reason)
    ("rm ", "Use /usr/bin/trash instead. Moves to Trash (recoverable). Example: /usr/bin/trash file.txt"),
    ("git checkout -- ", "Discards uncommitted changes permanently. Use 'git stash' first."),
    ("git reset --hard", "Destroys all uncommitted work. Use 'git stash' first."),
    ("git clean -f", "Deletes untracked files permanently. Use 'git clean -n' to preview first."),
    ("git push --force", "Overwrites remote history. Use '--force-with-lease' instead."),
    ("git push -f", "Overwrites remote history. Use '--force-with-lease' instead."),
    ("git branch -D", "Force-deletes branch without merge check. Use '-d' for safety."),
    ("git stash drop", "Permanently deletes stashed changes."),
    ("git stash clear", "Permanently deletes ALL stashed changes."),
    ("git restore ", "Can discard uncommitted changes. Be careful."),
    ("--no-verify", "Skips git hooks. Hooks enforce quality gates."),
    ("--no-gpg-sign", "Skips commit signing. May violate repo policy."),
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

def get_current_branch() -> str | None:
    """Get current git branch name, or None if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def is_protected_branch(branch: str | None) -> bool:
    """Check if branch is a protected main branch."""
    if not branch:
        return False
    return branch in ("main", "master")


def check_merge_protection(cmd: str) -> tuple[bool, str]:
    """
    Block all git merge commands.
    Merges should be done manually to avoid accidental conflicts.
    """
    if re.match(r"^git\s+merge\b", cmd):
        return True, (
            "git merge is blocked. "
            "Merges can create unexpected conflicts. "
            "Run this manually if needed."
        )

    return False, ""


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

    # Check merge protection (branch-aware)
    blocked, reason = check_merge_protection(cmd)
    if blocked:
        return True, reason

    # Check destructive patterns
    for pattern, reason in DESTRUCTIVE:
        if pattern in cmd:
            return True, reason

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
