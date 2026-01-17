#!/usr/bin/env python3
"""
audit-stripe-config.py

Full Stripe configuration audit.
Checks webhook endpoints, env vars, recent event delivery.

Requires: STRIPE_SECRET_KEY env var or .env.local file
Usage: python3 audit-stripe-config.py [--domain example.com]
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def get_stripe_key() -> str | None:
    """Get Stripe secret key from env or .env files."""
    key = os.environ.get("STRIPE_SECRET_KEY")
    if key:
        return key.strip()

    # Try .env files
    for env_file in [".env.local", ".env"]:
        path = Path(env_file)
        if path.exists():
            content = path.read_text()
            match = re.search(r'^STRIPE_SECRET_KEY=(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip().strip('"').strip("'")

    return None


def run_stripe_cmd(args: list[str], api_key: str) -> dict | None:
    """Run stripe CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["stripe"] + args + ["--api-key", api_key],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"{RED}Stripe CLI error:{NC} {result.stderr}", file=sys.stderr)
            return None
    except FileNotFoundError:
        print(f"{RED}Stripe CLI not installed.{NC} Install: brew install stripe/stripe-cli/stripe")
        return None
    except subprocess.TimeoutExpired:
        print(f"{RED}Stripe CLI timed out.{NC}")
        return None
    except json.JSONDecodeError:
        return None


def check_webhook_endpoints(api_key: str, domain: str | None) -> int:
    """Check webhook endpoint configuration."""
    print("\n== Webhook Endpoints ==\n")

    endpoints = run_stripe_cmd(["webhook_endpoints", "list"], api_key)
    if not endpoints:
        print(f"{RED}Could not fetch webhook endpoints.{NC}")
        return 1

    data = endpoints.get("data", [])
    if not data:
        print(f"{YELLOW}No webhook endpoints configured.{NC}")
        return 1

    issues = 0
    domain_endpoints = []

    for ep in data:
        url = ep.get("url", "")
        status = ep.get("status", "unknown")
        events = ep.get("enabled_events", [])

        # Filter by domain if specified
        if domain and domain not in url:
            continue

        domain_endpoints.append(ep)

        print(f"Endpoint: {url}")
        print(f"  Status: {status}")
        print(f"  Events: {len(events)} enabled")

        # Check for issues
        if status != "enabled":
            print(f"  {RED}ISSUE: Status is not 'enabled'{NC}")
            issues += 1

        # Check for redirects
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-I", "-X", "POST", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            http_status = result.stdout.strip()
            if http_status.startswith("3"):
                print(f"  {RED}ISSUE: URL redirects ({http_status}){NC}")
                issues += 1
            else:
                print(f"  {GREEN}No redirect (HTTP {http_status}){NC}")
        except Exception:
            print(f"  {YELLOW}Could not check for redirects{NC}")

        print()

    if domain:
        if len(domain_endpoints) == 0:
            print(f"{RED}No endpoints found for domain '{domain}'{NC}")
            issues += 1
        elif len(domain_endpoints) > 1:
            print(f"{YELLOW}Multiple endpoints for domain '{domain}' - may cause duplicate processing{NC}")

    return issues


def check_recent_events(api_key: str) -> int:
    """Check recent event delivery status."""
    print("\n== Recent Event Delivery ==\n")

    events = run_stripe_cmd(["events", "list", "--limit", "10"], api_key)
    if not events:
        print(f"{YELLOW}Could not fetch recent events.{NC}")
        return 0

    data = events.get("data", [])
    if not data:
        print("No recent events.")
        return 0

    pending_count = 0
    for event in data:
        pending = event.get("pending_webhooks", 0)
        if pending > 0:
            pending_count += 1
            event_type = event.get("type", "unknown")
            event_id = event.get("id", "unknown")
            print(f"{YELLOW}Pending:{NC} {event_type} ({event_id}) - {pending} pending webhooks")

    if pending_count == 0:
        print(f"{GREEN}All recent events delivered successfully.{NC}")
    else:
        print(f"\n{YELLOW}{pending_count} events with pending webhooks.{NC}")
        print("This may indicate delivery failures.")

    return pending_count


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audit Stripe configuration")
    parser.add_argument("--domain", help="Filter endpoints by domain")
    args = parser.parse_args()

    print("=" * 50)
    print("STRIPE CONFIGURATION AUDIT")
    print("=" * 50)

    api_key = get_stripe_key()
    if not api_key:
        print(f"{RED}STRIPE_SECRET_KEY not found.{NC}")
        print("Set via environment or .env.local file.")
        sys.exit(1)

    # Validate key format
    if not re.match(r'^sk_(test|live)_', api_key):
        print(f"{RED}Invalid STRIPE_SECRET_KEY format.{NC}")
        sys.exit(1)

    key_mode = "LIVE" if "_live_" in api_key else "TEST"
    print(f"\nUsing {key_mode} mode key")

    issues = 0
    issues += check_webhook_endpoints(api_key, args.domain)
    issues += check_recent_events(api_key)

    print("\n" + "=" * 50)
    if issues > 0:
        print(f"{RED}AUDIT FOUND {issues} ISSUE(S){NC}")
        sys.exit(1)
    else:
        print(f"{GREEN}AUDIT PASSED{NC}")
        sys.exit(0)


if __name__ == "__main__":
    main()
