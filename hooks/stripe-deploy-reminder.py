#!/usr/bin/env python3
"""
Stripe deploy verification hook for Claude Code.

When deploying projects with Stripe integration:
1. Verifies webhook URLs don't redirect (Stripe won't follow redirects)
2. Checks env var configuration
3. BLOCKS deploy if critical issues found

PreToolUse hook - runs before Bash commands execute.
"""
import json
import os
import re
import subprocess
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

    for env_file in ['.env.local', '.env', '.env.example']:
        path = cwd / env_file
        if path.exists():
            try:
                content = path.read_text()
                if any(ind in content for ind in STRIPE_INDICATORS):
                    return True
            except Exception:
                pass

    return False


def get_webhook_urls() -> list[str]:
    """Get webhook URLs from Stripe CLI."""
    try:
        result = subprocess.run(
            ['stripe', 'webhook_endpoints', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return []

        # Extract URLs from JSON output
        urls = re.findall(r'"url":\s*"(https://[^"]+)"', result.stdout)
        return urls
    except Exception:
        return []


def check_url_for_redirect(url: str) -> tuple[bool, str | None]:
    """
    Check if URL returns a redirect.
    Returns (has_redirect, redirect_location).
    """
    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-I', '-X', 'POST', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        http_code = result.stdout.strip()

        if http_code.startswith('3'):
            # Get redirect location
            loc_result = subprocess.run(
                ['curl', '-s', '-I', '-X', 'POST', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            for line in loc_result.stdout.split('\n'):
                if line.lower().startswith('location:'):
                    return True, line.split(':', 1)[1].strip()
            return True, None

        return False, None
    except Exception:
        return False, None  # Can't check, allow through


def verify_webhook_urls() -> tuple[bool, str]:
    """
    Verify all webhook URLs don't redirect.
    Returns (all_passed, message).
    """
    urls = get_webhook_urls()

    if not urls:
        return True, "No webhook URLs found to verify"

    issues = []
    for url in urls:
        has_redirect, redirect_to = check_url_for_redirect(url)
        if has_redirect:
            if redirect_to:
                issues.append(f"  {url}\n    → Redirects to: {redirect_to}")
            else:
                issues.append(f"  {url}\n    → Returns 3xx redirect")

    if issues:
        message = [
            "WEBHOOK URL REDIRECT DETECTED",
            "",
            "Stripe does NOT follow redirects for POST webhooks.",
            "These webhook URLs will silently fail:",
            "",
            *issues,
            "",
            "FIX: Update webhook to use canonical domain:",
            "  stripe webhook_endpoints update <id> --url \"<canonical_url>\"",
            "",
            "Deploy BLOCKED until fixed."
        ]
        return False, "\n".join(message)

    return True, f"✓ All {len(urls)} webhook URLs verified (no redirects)"


def check_command(cmd: str) -> tuple[str, bool, str]:
    """
    Check if command is a deploy and project has Stripe integration.
    Returns (action, should_output, message).
    action: "block", "warn", or "allow"
    """
    if not cmd:
        return "allow", False, ""

    # Check if this is a deploy command
    is_deploy = any(re.search(p, cmd, re.IGNORECASE) for p in DEPLOY_PATTERNS)
    if not is_deploy:
        return "allow", False, ""

    # Check if project has Stripe integration
    if not has_stripe_integration():
        return "allow", False, ""

    # Verify webhook URLs for redirects
    urls_passed, urls_message = verify_webhook_urls()

    if not urls_passed:
        return "block", True, urls_message

    # All checks passed, show confirmation and proceed
    message_parts = [
        "STRIPE VERIFICATION PASSED",
        "",
        urls_message,
        "",
        "Proceeding with deploy."
    ]

    return "warn", True, "\n".join(message_parts)


def block(cmd: str, reason: str) -> None:
    """Block command execution with error message."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "decision": "block",
            "message": f"🛑 {reason}\n\nCommand blocked: {cmd}"
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def warn(cmd: str, reason: str) -> None:
    """Output warning and allow command to proceed."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "message": f"✅ {reason}\n\nCommand: {cmd}"
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

    action, should_output, reason = check_command(cmd)

    if action == "block":
        block(cmd, reason)
    elif should_output:
        warn(cmd, reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
