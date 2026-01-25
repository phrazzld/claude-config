#!/usr/bin/env python3
"""
Vercel environment guard for Claude Code.

Requires explicit --environment flag for env mutations (add/rm).
Allows all other commands including explicit prod deploys.

PreToolUse hook - runs before Bash commands execute.
"""
import json
import re
import sys

# Safe patterns - always allowed without checks
SAFE_PATTERNS = [
    r"^(npx\s+)?vercel\s+(--)?help",
    r"^(npx\s+)?vercel\s+(-v|--version)",
    r"^(npx\s+)?vercel\s+(ls|list|inspect|logs|whoami)\b",
    r"^(npx\s+)?vercel\s+domains\s+ls\b",
    r"^(npx\s+)?vercel\s+env\s+(ls|list|pull)\b",
    r"^(npx\s+)?vercel\s+(login|logout|link|dev)\b",
    r"^(npx\s+)?vercel\s+deploy\b",  # deploys are fine (preview default or explicit prod)
    r"^(npx\s+)?vercel\s*$",          # just 'vercel' shows project info
]

# Env mutation patterns - require explicit environment
ENV_MUTATION_PATTERNS = [
    r"^(npx\s+)?vercel\s+env\s+(add|rm|remove)\b",
]

# Match either --environment=xxx flag OR positional environment arg
# Positional: vercel env add VAR production OR vercel env add VAR preview
HAS_ENVIRONMENT = re.compile(r"(--environment[=\s]+\w+|\b(production|preview|development)\b)")


def check_command(cmd: str) -> tuple[bool, str]:
    """
    Check Vercel command for environment clarity.
    Returns (should_block, reason).
    """
    if not cmd:
        return False, ""

    # Only check vercel commands
    if not re.search(r"\bvercel\b", cmd):
        return False, ""

    # Safe patterns pass through
    for pattern in SAFE_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return False, ""

    # Env mutations need explicit target
    for pattern in ENV_MUTATION_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            if not HAS_ENVIRONMENT.search(cmd):
                return True, (
                    "Vercel env command needs explicit environment.\n\n"
                    "Use:\n"
                    "  vercel env add VAR --environment=production\n"
                    "  vercel env add VAR --environment=preview\n"
                    "  vercel env add VAR --environment=development"
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
