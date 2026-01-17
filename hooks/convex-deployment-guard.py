#!/usr/bin/env python3
"""
Convex deployment clarity guard for Claude Code.

Warns when Convex CLI commands might be ambiguous about which deployment
they're targeting. The CONVEX_DEPLOY_KEY env var takes precedence over
--prod flag and CONVEX_DEPLOYMENT prefix, which can cause confusion.

PreToolUse hook - runs before Bash commands execute.
"""
import json
import os
import re
import sys

# Patterns that indicate Convex CLI usage
CONVEX_PATTERNS = [
    r'\bnpx\s+convex\b',      # npx convex ...
    r'\bconvex\s+run\b',       # convex run ...
    r'\bconvex\s+env\b',       # convex env ...
    r'\bconvex\s+data\b',      # convex data ...
    r'\bconvex\s+deploy\b',    # convex deploy ...
]

# Patterns that suggest user is trying to target prod
PROD_INTENT_PATTERNS = [
    r'--prod\b',
    r'CONVEX_DEPLOYMENT=prod',
]


def check_command(cmd: str) -> tuple[bool, str]:
    """
    Check if command uses Convex CLI with potential deployment ambiguity.
    Returns (should_warn, warning_message).
    """
    if not cmd:
        return False, ""

    # Check if this is a Convex command
    is_convex_cmd = any(re.search(p, cmd, re.IGNORECASE) for p in CONVEX_PATTERNS)
    if not is_convex_cmd:
        return False, ""

    # Check if user seems to be targeting prod
    intends_prod = any(re.search(p, cmd, re.IGNORECASE) for p in PROD_INTENT_PATTERNS)

    # Check if CONVEX_DEPLOY_KEY is set in environment
    has_deploy_key = bool(os.environ.get("CONVEX_DEPLOY_KEY"))

    if intends_prod and has_deploy_key:
        # User intends prod but CONVEX_DEPLOY_KEY will override
        return True, (
            "CONVEX_DEPLOY_KEY is set in your environment.\n\n"
            "This takes precedence over --prod flag and CONVEX_DEPLOYMENT prefix.\n"
            "The command will use the deployment specified in CONVEX_DEPLOY_KEY,\n"
            "which may or may not be prod.\n\n"
            "To verify which deployment you're targeting:\n"
            "  1. Check CONVEX_DEPLOY_KEY value (starts with 'prod:' or 'dev:')\n"
            "  2. Or unset CONVEX_DEPLOY_KEY and use --prod flag\n\n"
            "Proceeding with command - just be aware of this."
        )

    if not intends_prod:
        # Check if they're running a query/mutation without specifying env
        if re.search(r'\bconvex\s+run\b', cmd) and not has_deploy_key:
            if not re.search(r'--prod|--dev|--preview', cmd, re.IGNORECASE):
                return True, (
                    "Running Convex command without explicit deployment target.\n\n"
                    "This will use your default deployment (likely dev).\n"
                    "If you intended to target production, add --prod flag.\n\n"
                    "Proceeding with command."
                )

    return False, ""


def warn(cmd: str, reason: str) -> None:
    """Output warning and allow command to proceed."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "message": f"⚠️  CONVEX DEPLOYMENT WARNING:\n\n{reason}\n\nCommand: {cmd}"
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

    should_warn, reason = check_command(cmd)

    if should_warn:
        warn(cmd, reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
