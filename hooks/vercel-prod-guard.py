#!/usr/bin/env python3
"""
Vercel production deployment guard for Claude Code.

Blocks direct `vercel --prod` commands to prevent deploying unmerged branches
to production. Production deploys should only happen via git push to master.

PreToolUse hook - runs before Bash commands execute.
"""
import json
import re
import sys

# Patterns that indicate production deployment
PROD_PATTERNS = [
    r'\bvercel\b.*\s--prod\b',           # vercel --prod, vercel deploy --prod
    r'\bvercel\b.*\s-p\b',               # vercel -p (short flag)
    r'\bvercel\b.*--production\b',       # vercel --production
    r'\bnpx\s+vercel\b.*\s--prod\b',     # npx vercel --prod
    r'\bnpx\s+vercel\b.*\s-p\b',         # npx vercel -p
    r'\bvercel\s+deploy\s+--prod\b',     # vercel deploy --prod
    r'\bvercel\s+--prod\s+deploy\b',     # vercel --prod deploy
]


def check_command(cmd: str) -> tuple[bool, str]:
    """
    Check if command deploys to Vercel production.
    Returns (should_block, reason).
    """
    if not cmd:
        return False, ""

    for pattern in PROD_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return True, (
                "Direct production deploys are blocked.\n\n"
                "Production should only be deployed via git push to master:\n"
                "  git checkout master && git merge <branch> && git push\n\n"
                "Or merge via GitHub PR, which triggers auto-deploy.\n\n"
                "This prevents deploying unmerged feature branches to production."
            )

    return False, ""


def deny(cmd: str, reason: str) -> None:
    """Output deny decision and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"BLOCKED: {reason}\n\n"
                f"Command: {cmd}"
            )
        }
    }
    print(json.dumps(output))
    sys.exit(0)


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
        deny(cmd, reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
