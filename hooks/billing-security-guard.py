#!/usr/bin/env python3
"""
Billing security guard for Claude Code.

Prevents common billing integration mistakes:
1. Hardcoded API keys in code
2. Billing env vars set without --prod flag

PreToolUse hook - runs before Bash/Edit/Write commands.
"""
import json
import re
import sys

# API key patterns that should NEVER appear in code
HARDCODED_KEY_PATTERNS = [
    (r'sk_live_[a-zA-Z0-9]{20,}', "Stripe live secret key"),
    (r'sk_test_[a-zA-Z0-9]{20,}', "Stripe test secret key"),
    (r'pk_live_[a-zA-Z0-9]{20,}', "Stripe live publishable key"),
    (r'whsec_[a-zA-Z0-9]{20,}', "Stripe webhook secret"),
    (r'rk_live_[a-zA-Z0-9]{20,}', "Stripe restricted key"),
]

# Billing-related env var names
BILLING_ENV_VARS = [
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "STRIPE_SYNC_SECRET",
    "STRIPE_PUBLISHABLE_KEY",
    "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY",
]


def check_hardcoded_keys(content: str) -> tuple[bool, str]:
    """Check if content contains hardcoded API keys."""
    if not content:
        return False, ""

    for pattern, key_type in HARDCODED_KEY_PATTERNS:
        match = re.search(pattern, content)
        if match:
            # Don't block if it's in a comment explaining the format
            # But do block actual key values
            key_preview = match.group(0)[:15] + "..."
            return True, (
                f"Detected hardcoded {key_type}: {key_preview}\n\n"
                "API keys should NEVER be hardcoded in source code.\n"
                "Use environment variables instead:\n"
                "  process.env.STRIPE_SECRET_KEY\n\n"
                "If this is documentation showing the format, use a placeholder like:\n"
                "  sk_test_XXXXXXXXXXXXXXXX"
            )

    return False, ""


def check_billing_env_command(cmd: str) -> tuple[bool, str]:
    """Check if setting billing env vars without --prod flag."""
    if not cmd:
        return False, ""

    # Check if this is a convex env set command
    if not re.search(r'\bconvex\s+env\s+set\b', cmd, re.IGNORECASE):
        return False, ""

    # Check if it involves a billing env var
    billing_var_used = None
    for var in BILLING_ENV_VARS:
        if var in cmd:
            billing_var_used = var
            break

    if not billing_var_used:
        return False, ""

    # Check if --prod flag is present
    if re.search(r'--prod\b', cmd):
        return False, ""

    return True, (
        f"Setting billing env var '{billing_var_used}' without --prod flag.\n\n"
        "This will only set the variable on your DEV deployment.\n"
        "Billing env vars usually need to be set on PROD too.\n\n"
        "Did you mean:\n"
        f"  npx convex env set --prod {billing_var_used} <value>\n\n"
        "If you intentionally want dev-only, proceed. Otherwise, add --prod."
    )


def block(reason: str) -> None:
    """Block the command."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def warn(reason: str) -> None:
    """Warn but allow the command."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "message": f"⚠️  BILLING SECURITY WARNING:\n\n{reason}"
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    # Check Edit/Write for hardcoded keys
    if tool_name in ("Edit", "Write", "MultiEdit"):
        content = tool_input.get("content", "") or tool_input.get("new_string", "")
        should_block, reason = check_hardcoded_keys(content)
        if should_block:
            block(reason)

    # Check Bash for billing env var commands
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        should_warn, reason = check_billing_env_command(cmd)
        if should_warn:
            warn(reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
