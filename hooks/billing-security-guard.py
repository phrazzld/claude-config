#!/usr/bin/env python3
"""
Billing security guard for Claude Code.

Prevents common billing integration mistakes:
1. Hardcoded API keys in code
2. Billing env vars set without --prod flag
3. LIVE keys set to DEV deployments (BLOCKED)
4. TEST keys set to PROD deployments (BLOCKED)

PreToolUse hook - runs before Bash/Edit/Write commands.

Postmortem: 2026-01-22 - Live Stripe keys in Convex DEV for 5 days.
Root cause: Hook warned but didn't block environment mismatches.
"""
import json
import re
import sys

# API key patterns that should NEVER appear in code (but OK in .env files)
HARDCODED_KEY_PATTERNS = [
    (r'sk_live_[a-zA-Z0-9]{20,}', "Stripe live secret key"),
    (r'sk_test_[a-zA-Z0-9]{20,}', "Stripe test secret key"),
    (r'pk_live_[a-zA-Z0-9]{20,}', "Stripe live publishable key"),
    (r'whsec_[a-zA-Z0-9]{20,}', "Stripe webhook secret"),
    (r'rk_live_[a-zA-Z0-9]{20,}', "Stripe restricted key"),
]

# File patterns where API keys ARE allowed (environment files)
ENV_FILE_PATTERNS = [
    r'\.env$',
    r'\.env\.local$',
    r'\.env\.[a-zA-Z]+$',  # .env.development, .env.production, etc.
    r'\.env\.example$',    # Allow examples too (they use placeholders usually)
]


def is_env_file(file_path: str) -> bool:
    """Check if the file path is an environment file where keys are allowed."""
    if not file_path:
        return False
    import os
    basename = os.path.basename(file_path)
    for pattern in ENV_FILE_PATTERNS:
        if re.match(pattern, basename):
            return True
    return False

# Billing-related env var names that use live/test distinction
BILLING_ENV_VARS_WITH_MODE = [
    "STRIPE_SECRET_KEY",
    "STRIPE_PUBLISHABLE_KEY",
    "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY",
]

# Billing env vars that don't have live/test distinction
BILLING_ENV_VARS_NO_MODE = [
    "STRIPE_WEBHOOK_SECRET",
    "STRIPE_SYNC_SECRET",
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


def extract_key_value_from_cmd(cmd: str, var_name: str) -> str | None:
    """
    Extract the value being set for an env var from a convex env set command.
    Handles quoted and unquoted values.
    """
    # Pattern: convex env set [--prod] VAR_NAME "value" or VAR_NAME value
    # The value comes after the var name
    patterns = [
        # Quoted value: VAR_NAME "value" or VAR_NAME 'value'
        rf'{var_name}\s+["\']([^"\']+)["\']',
        # Unquoted value: VAR_NAME value (capture until space or end)
        rf'{var_name}\s+([^\s"\']+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, cmd)
        if match:
            return match.group(1)

    return None


def check_env_mode_mismatch(cmd: str) -> tuple[str, str]:
    """
    Check for environment mode mismatches:
    - LIVE keys → DEV deployment = BLOCK
    - TEST keys → PROD deployment = BLOCK

    Returns: (action, reason) where action is 'block', 'warn', or 'allow'
    """
    if not cmd:
        return 'allow', ""

    # Check if this is a convex env set command
    if not re.search(r'\bconvex\s+env\s+set\b', cmd, re.IGNORECASE):
        return 'allow', ""

    # Determine target environment
    is_prod_target = bool(re.search(r'--prod\b', cmd))

    # Check each billing env var
    for var in BILLING_ENV_VARS_WITH_MODE:
        if var not in cmd:
            continue

        value = extract_key_value_from_cmd(cmd, var)
        if not value:
            continue

        # Detect key mode from value
        is_live_key = bool(re.search(r'(sk_live_|pk_live_|rk_live_)', value))
        is_test_key = bool(re.search(r'(sk_test_|pk_test_|rk_test_)', value))

        if is_live_key and not is_prod_target:
            return 'block', (
                f"🚨 BLOCKED: Setting LIVE key to DEV deployment!\n\n"
                f"Variable: {var}\n"
                f"Key type: LIVE (sk_live_/pk_live_)\n"
                f"Target: DEV (no --prod flag)\n\n"
                "LIVE keys should ONLY be set to production:\n"
                f"  npx convex env set --prod {var} \"<live_value>\"\n\n"
                "For dev deployment, use TEST keys (sk_test_/pk_test_).\n\n"
                "If this is intentional (testing prod keys locally), you must:\n"
                "1. Acknowledge the risk\n"
                "2. Manually run the command outside Claude Code"
            )

        if is_test_key and is_prod_target:
            return 'block', (
                f"🚨 BLOCKED: Setting TEST key to PROD deployment!\n\n"
                f"Variable: {var}\n"
                f"Key type: TEST (sk_test_/pk_test_)\n"
                f"Target: PROD (--prod flag present)\n\n"
                "TEST keys should NOT be set to production.\n"
                "Use LIVE keys for production:\n"
                f"  npx convex env set --prod {var} \"<live_value>\"\n\n"
                "If you need to test in prod (staging), consider:\n"
                "1. Using a separate Stripe account for staging\n"
                "2. Creating a dedicated Convex preview deployment"
            )

    return 'allow', ""


def check_billing_env_command(cmd: str) -> tuple[bool, str]:
    """Check if setting billing env vars without --prod flag (warning only)."""
    if not cmd:
        return False, ""

    # Check if this is a convex env set command
    if not re.search(r'\bconvex\s+env\s+set\b', cmd, re.IGNORECASE):
        return False, ""

    # Check if it involves a billing env var
    billing_var_used = None
    for var in BILLING_ENV_VARS_WITH_MODE + BILLING_ENV_VARS_NO_MODE:
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

    # Check Edit/Write for hardcoded keys (but allow in .env files)
    if tool_name in ("Edit", "Write", "MultiEdit"):
        file_path = tool_input.get("file_path", "")
        # Skip check for environment files - that's where keys belong
        if not is_env_file(file_path):
            content = tool_input.get("content", "") or tool_input.get("new_string", "")
            should_block, reason = check_hardcoded_keys(content)
            if should_block:
                block(reason)

    # Check Bash for billing env var commands
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")

        # First check for environment mode mismatch (BLOCKING)
        action, reason = check_env_mode_mismatch(cmd)
        if action == 'block':
            block(reason)

        # Then check for missing --prod flag (WARNING)
        should_warn, reason = check_billing_env_command(cmd)
        if should_warn:
            warn(reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
