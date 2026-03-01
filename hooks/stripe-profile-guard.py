#!/usr/bin/env python3
"""
Stripe CLI profile guard for Claude Code.

Blocks stripe commands without explicit -p/--project-name flag.
Forces explicit environment targeting to prevent sandbox/production confusion.

TWO STRIPE ACCOUNTS (test mode is DEPRECATED):
- Sandbox (acct_1SV2rGD4aITn8Hia): Completely separate account for development.
  Use: stripe -p sandbox ...
- Production (acct_1SV2rADIyumDtWyU): Real money. ALWAYS use --live flag.
  Use: stripe -p production ... --live

NEVER use sk_test_* keys from the production account. Stripe deprecated
test mode in favor of fully isolated sandbox accounts. If you need to test,
use the sandbox account (profile: sandbox), not test-mode keys.
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
            "TWO ACCOUNTS (test mode is DEPRECATED):\n"
            "  stripe -p sandbox ...            # Sandbox account (development)\n"
            "  stripe -p production ... --live  # Production account (real money)\n\n"
            "NEVER use sk_test_* from production account.\n"
            "To check profiles: stripe config --list"
        )

    # Extract profile name
    profile = profile_match.group(1) or profile_match.group(2)

    # Production profile requires --live flag
    if profile == "production" and not HAS_LIVE_FLAG.search(cmd):
        return True, (
            "Production profile requires --live flag.\n\n"
            "Stripe test mode is DEPRECATED. The production account must ALWAYS\n"
            "use --live. For development, use the sandbox account instead:\n"
            "  stripe -p sandbox ...\n\n"
            "Production (live mode):\n"
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
