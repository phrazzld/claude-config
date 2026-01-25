#!/usr/bin/env python3
"""
Convex deployment guard for Claude Code.

Blocks unreliable patterns (CONVEX_DEPLOYMENT prefix) and requires
explicit --prod or --preview flag for deploy commands.

PreToolUse hook - runs before Bash commands execute.
"""
import json
import re
import sys


def check_command(cmd: str) -> tuple[str, str]:
    """
    Check Convex command for deployment clarity.
    Returns (action, reason) where action is 'block', 'warn', or 'allow'.
    """
    if not cmd:
        return 'allow', ""

    # Only check commands with convex
    if not re.search(r"\bconvex\b", cmd, re.IGNORECASE):
        return 'allow', ""

    # BLOCK: CONVEX_DEPLOYMENT=prod:xxx pattern (unreliable)
    if re.search(r"CONVEX_DEPLOYMENT=prod:", cmd):
        return 'block', (
            "CONVEX_DEPLOYMENT=prod:xxx prefix is unreliable.\n\n"
            "Use --prod flag instead:\n"
            "  npx convex env set --prod VAR value\n"
            "  npx convex deploy --prod\n"
            "  npx convex env ls --prod"
        )

    # BLOCK: deploy without explicit confirmation
    # Note: `convex deploy` defaults to production, use -y to confirm
    if re.search(r"\bconvex\s+deploy\b", cmd):
        if not re.search(r"(-y|--yes|--preview)\b", cmd):
            return 'block', (
                "Convex deploy needs explicit confirmation.\n\n"
                "Use:\n"
                "  npx convex deploy -y          # production (default)\n"
                "  npx convex deploy --preview   # preview deployment"
            )

    # Allow everything else (env set defaults to dev, which is recoverable)
    return 'allow', ""


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

    action, reason = check_command(cmd)

    if action == 'block':
        deny(cmd, reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
