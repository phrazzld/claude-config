#!/usr/bin/env python3
"""
Stripe deploy reminder hook for Claude Code.

Warns when deploying projects that have Stripe integration, reminding
to verify config before production deployment.

PreToolUse hook - runs before Bash commands execute.
"""
import json
import os
import re
import sys
from pathlib import Path

# Deploy command patterns
DEPLOY_PATTERNS = [
    r'\bvercel\s+deploy\b',
    r'\bvercel\s+--prod\b',
    r'\bvercel\s+.*--prod\b',
    r'\bnpx\s+convex\s+deploy\b',
    r'\bconvex\s+deploy\b',
]

# Stripe indicators in env files
STRIPE_INDICATORS = ['STRIPE_', 'NEXT_PUBLIC_STRIPE']


def has_stripe_integration() -> bool:
    """Check if current project has Stripe integration."""
    cwd = Path.cwd()

    # Check .env.local
    env_local = cwd / '.env.local'
    if env_local.exists():
        try:
            content = env_local.read_text()
            if any(ind in content for ind in STRIPE_INDICATORS):
                return True
        except Exception:
            pass

    # Check .env
    env_file = cwd / '.env'
    if env_file.exists():
        try:
            content = env_file.read_text()
            if any(ind in content for ind in STRIPE_INDICATORS):
                return True
        except Exception:
            pass

    # Check .env.example
    env_example = cwd / '.env.example'
    if env_example.exists():
        try:
            content = env_example.read_text()
            if any(ind in content for ind in STRIPE_INDICATORS):
                return True
        except Exception:
            pass

    return False


def has_verification_script() -> bool:
    """Check if verification script exists."""
    cwd = Path.cwd()
    return (cwd / 'scripts' / 'verify-env.sh').exists()


def check_command(cmd: str) -> tuple[bool, str]:
    """
    Check if command is a deploy and project has Stripe integration.
    Returns (should_warn, warning_message).
    """
    if not cmd:
        return False, ""

    # Check if this is a deploy command
    is_deploy = any(re.search(p, cmd, re.IGNORECASE) for p in DEPLOY_PATTERNS)
    if not is_deploy:
        return False, ""

    # Check if project has Stripe integration
    if not has_stripe_integration():
        return False, ""

    # Build warning message
    has_script = has_verification_script()

    message_parts = [
        "STRIPE INTEGRATION DETECTED",
        "",
        "Before deploying, verify:",
        "1. Env vars set on PRODUCTION (not just dev)",
        "2. Webhook URL uses canonical domain (no redirects)",
        "3. No trailing whitespace in secrets",
    ]

    if has_script:
        message_parts.extend([
            "",
            "Run verification:",
            "  ./scripts/verify-env.sh --prod-only"
        ])
    else:
        message_parts.extend([
            "",
            "No verification script found.",
            "Consider creating scripts/verify-env.sh",
            "See: ~/.claude/skills/external-integration-patterns/SKILL.md"
        ])

    message_parts.extend([
        "",
        "Proceeding with deploy."
    ])

    return True, "\n".join(message_parts)


def warn(cmd: str, reason: str) -> None:
    """Output warning and allow command to proceed."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "message": f"⚠️  {reason}\n\nCommand: {cmd}"
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
