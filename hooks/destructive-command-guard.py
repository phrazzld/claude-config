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

# Regex patterns for commands that need smarter matching
# These match the command only when it appears as an actual command invocation,
# not as a substring inside strings, commit messages, or other content.
#
# Matches: rm file, ls && rm file, $(rm file), `rm file`, ; rm file, | xargs rm
# Does NOT match: git commit -m "form optimization", echo "inform user"
RM_COMMAND_PATTERN = re.compile(
    r'(^|[;&|`]|\$\()\s*rm\s',
    re.MULTILINE
)

# Simple substring patterns - these are specific enough to not need regex
# (they won't accidentally match normal text)
DESTRUCTIVE_SUBSTRINGS = [
    # Git commands
    ("git checkout -- ", "Discards uncommitted changes permanently. Use 'git stash' first."),
    ("git reset --hard", "Destroys all uncommitted work. Use 'git stash' first."),
    ("git clean -f", "Deletes untracked files permanently. Use 'git clean -n' to preview first."),
    ("git push --force", "Overwrites remote history. Use '--force-with-lease' instead."),
    ("git push -f ", "Overwrites remote history. Use '--force-with-lease' instead."),
    ("git branch -D ", "Force-deletes branch without merge check. Use '-d' for safety."),
    ("git stash drop", "Permanently deletes stashed changes."),
    ("git stash clear", "Permanently deletes ALL stashed changes."),
    # GitHub CLI commands - equally destructive as their git equivalents
    ("gh pr merge", "Merges PR and may delete branch. Run manually to review."),
    ("gh repo delete", "Permanently deletes repository. Extremely destructive."),
    ("gh release delete", "Permanently deletes a release."),
    ("gh issue delete", "Permanently deletes an issue."),
    ("gh repo archive", "Archives repository, making it read-only."),
]

# Patterns that need word boundary checking (could appear in strings)
DESTRUCTIVE_PATTERNS = [
    # (regex_pattern, reason)
    (re.compile(r'(^|[;&|`]|\$\()\s*git\s+restore\s+(?!--staged|-S)'),
     "git restore can discard uncommitted changes. Use 'git restore --staged' for safe unstaging."),
]

# Flags that are dangerous anywhere in the command
DANGEROUS_FLAGS = [
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


def strip_quoted_content(cmd: str) -> str:
    """
    Remove content inside quotes to avoid false positives from string literals.
    Handles both single and double quotes, and escaped quotes.

    Example: git commit -m "rm all files" -> git commit -m ""
    """
    result = []
    i = 0
    in_single = False
    in_double = False

    while i < len(cmd):
        char = cmd[i]

        # Handle escape sequences
        if char == '\\' and i + 1 < len(cmd):
            if not in_single and not in_double:
                result.append(char)
                result.append(cmd[i + 1])
            i += 2
            continue

        # Handle quote transitions
        if char == '"' and not in_single:
            in_double = not in_double
            result.append(char)  # Keep the quote itself
        elif char == "'" and not in_double:
            in_single = not in_single
            result.append(char)  # Keep the quote itself
        elif not in_single and not in_double:
            result.append(char)
        # If inside quotes, don't append (strip the content)

        i += 1

    return ''.join(result)


def check_command(cmd: str) -> tuple[bool, str]:
    """
    Check if command should be blocked.
    Returns (should_block, reason).
    """
    if not cmd:
        return False, ""

    # Check safe patterns first (allowlist) - check original command
    for safe in SAFE:
        if safe in cmd:
            return False, ""

    # Check merge protection (branch-aware)
    blocked, reason = check_merge_protection(cmd)
    if blocked:
        return True, reason

    # Strip quoted content to avoid false positives from commit messages,
    # echo statements, string literals, etc.
    cmd_stripped = strip_quoted_content(cmd)

    # Check rm command with smart pattern (avoids false positives in strings)
    if RM_COMMAND_PATTERN.search(cmd_stripped):
        return True, "Use /usr/bin/trash instead. Moves to Trash (recoverable). Example: /usr/bin/trash file.txt"

    # Check simple substring patterns (specific enough to not need regex)
    for pattern, reason in DESTRUCTIVE_SUBSTRINGS:
        if pattern in cmd_stripped:
            return True, reason

    # Check regex patterns (for commands that could appear in strings)
    for pattern, reason in DESTRUCTIVE_PATTERNS:
        if pattern.search(cmd_stripped):
            return True, reason

    # Check dangerous flags (these are dangerous anywhere, even in strings,
    # because they might be used in eval or variable expansion)
    for flag, reason in DANGEROUS_FLAGS:
        if flag in cmd:  # Check original, not stripped
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
