"""Sentry initialization with PII scrubbing."""

import os

import sentry_sdk


def init_sentry() -> None:
    """Initialize Sentry SDK. No-op when SENTRY_DSN is unset."""
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        return

    env = os.environ.get("SENTRY_ENVIRONMENT", "development")
    release = os.environ.get("SENTRY_RELEASE")

    sentry_sdk.init(
        dsn=dsn,
        environment=env,
        release=release,
        traces_sample_rate=0.1,
        send_default_pii=False,
        before_send=_scrub_pii,
    )


def _scrub_pii(event, hint):
    """Remove PII from Sentry events."""
    user = event.get("user", {})
    if "email" in user:
        user["email"] = "[REDACTED]"
    if "ip_address" in user:
        del user["ip_address"]
    return event
