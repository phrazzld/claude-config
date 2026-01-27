#!/usr/bin/env python3
"""
Stripe CLI profile guard for Claude Code.

Blocks stripe commands without explicit -p/--project-name flag.
Forces explicit environment targeting to prevent sandbox/production confusion.

IMPORTANT: Production profile requires --live flag.
- Sandbox account: isolated test environment, test mode is appropriate
- Production account: real money, ALWAYS use --live flag
"""
import json
import re
import sys

# Commands that are safe without profile (don't touch account data)
SAFE_PATTERNS = [
    r"^stripe\s+(--)?help",
    r"^stripe\s+-h\b",
    r"^stripe\s+help\b",
    r"^stripe\s+version",
    r"^stripe\s+-v\b",
    r"^stripe\s+--version",
    r"^stripe\s+completion",
    r"^stripe\s+config\s+--list",
    r"^stripe\s+-p\s+\w+\s+config\s+--list",
    r"^stripe\s+login",
]

HAS_PROFILE = re.compile(r"\s+-p\s+(\w+)|\s+--project-name[=\s]+(\w+)")
HAS_LIVE_FLAG = re.compile(r"\s+--live\b")


def check_command(cmd: str) -> tuple[bool, str]:
    if not cmd:
        return False, ""
    cmd = cmd.strip()
    if not re.match(r"^stripe\b", cmd):
        return False, ""
    for pattern in SAFE_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return False, ""

    # Check for profile flag
    profile_match = HAS_PROFILE.search(cmd)
    if not profile_match:
        return True, (
            "Stripe command without explicit profile (-p flag).\n\n"
            "Use:\n"
            "  stripe -p sandbox ...            # Development (test mode)\n"
            "  stripe -p production ... --live  # Production (live mode)\n\n"
            "To check profiles: stripe config --list"
        )

    # Extract profile name
    profile = profile_match.group(1) or profile_match.group(2)

    # Production profile requires --live flag
    if profile == "production" and not HAS_LIVE_FLAG.search(cmd):
        return True, (
            "Production profile requires --live flag.\n\n"
            "Stripe CLI defaults to test mode. Production account must use live mode.\n\n"
            "Use:\n"
            "  stripe -p production ... --live\n\n"
            "Example:\n"
            "  stripe -p production products list --live"
        )

    return False, ""


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    tool_input = data.get("tool_input") or {}
    cmd = tool_input.get("command", "")
    if not isinstance(cmd, str) or not cmd:
        sys.exit(0)
    should_block, reason = check_command(cmd)
    if should_block:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"BLOCKED: {reason}\n\nCommand: {cmd}",
            }
        }
        print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
