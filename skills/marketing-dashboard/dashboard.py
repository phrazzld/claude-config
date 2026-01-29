#!/usr/bin/env python3
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
import os
import sys
from typing import Any

import click

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
sys.path.insert(0, SRC_DIR)

from display import (  # noqa: E402
    print_error,
    print_heading,
    print_kv_table,
    print_section,
    print_table,
    print_warning,
    sparkline,
)
from gsc_client import query_search_analytics  # noqa: E402
from posthog_client import PostHogClient  # noqa: E402
from stripe_client import StripeClient  # noqa: E402


def _utc_today() -> date:
    return datetime.now(timezone.utc).date()


def _days_ago(days: int) -> date:
    return _utc_today() - timedelta(days=days)


def _format_money(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"${value:,.2f}"


def _parse_days(period: str) -> int:
    if period.endswith("d"):
        return int(period[:-1])
    raise click.BadParameter("period must end with d")


def _load_ads_metrics() -> dict[str, Any]:
    raw = os.environ.get("ADS_METRICS_JSON")
    path = os.environ.get("ADS_METRICS_PATH")
    if raw:
        return json.loads(raw)
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return {}


def _posthog_client() -> PostHogClient | None:
    try:
        return PostHogClient.from_env()
    except ValueError as exc:
        print_warning(str(exc))
        return None


def _stripe_client() -> StripeClient | None:
    try:
        return StripeClient.from_env()
    except ValueError as exc:
        print_warning(str(exc))
        return None


@click.group(name="mktg")
def cli() -> None:
    """Marketing dashboard CLI."""


@cli.command()
def status() -> None:
    """Quick overview: traffic (7d), revenue (30d), top errors."""
    print_heading("MARKETING STATUS")

    traffic = None
    traffic_series: list[float] = []
    errors: list[tuple[str, int]] = []
    posthog = _posthog_client()
    if posthog:
        trend = posthog.trend(["$pageview"], 7)
        result = trend.get("result") or []
        if result:
            traffic_series = result[0].get("data") or []
            traffic = int(sum(traffic_series))
        errors = posthog.top_breakdown("$exception", "$exception_message", 7, limit=5)

    revenue = None
    stripe_client = _stripe_client()
    if stripe_client:
        since = datetime.now(timezone.utc) - timedelta(days=30)
        revenue = stripe_client.revenue_total(since)

    print_kv_table(
        "Summary",
        [
            (
                "Traffic (7d)",
                f"{traffic:,} {sparkline(traffic_series)}" if traffic is not None else "n/a",
            ),
            ("Revenue (30d)", _format_money(revenue)),
        ],
    )

    if errors:
        print_table("Top errors (7d)", ["Error", "Count"], [(e, str(c)) for e, c in errors])
    else:
        print_section("Top errors (7d)")
        print_warning("No PostHog error data")


@cli.command()
@click.option("--period", type=click.Choice(["7d", "30d", "90d"]), default="30d", show_default=True)
def seo(period: str) -> None:
    """GSC metrics: clicks, impressions, avg position, top queries."""
    site_url = os.environ.get("GSC_SITE_URL")
    if not site_url:
        print_error("GSC_SITE_URL required")
        return
    days = _parse_days(period)
    start_date = _days_ago(days).isoformat()
    end_date = _utc_today().isoformat()
    rows = query_search_analytics(site_url, start_date, end_date, dimensions=["query"], row_limit=250)

    clicks = sum(row.get("clicks", 0) for row in rows)
    impressions = sum(row.get("impressions", 0) for row in rows)
    weighted_pos = sum((row.get("position", 0) * row.get("impressions", 0)) for row in rows)
    avg_position = (weighted_pos / impressions) if impressions else 0

    print_heading("SEO")
    print_kv_table(
        f"GSC totals ({period})",
        [
            ("Clicks", f"{clicks:,}"),
            ("Impressions", f"{impressions:,}"),
            ("Avg position", f"{avg_position:.2f}"),
        ],
    )

    top = sorted(rows, key=lambda r: r.get("clicks", 0), reverse=True)[:10]
    if top:
        print_table(
            "Top queries",
            ["Query", "Clicks", "Impressions", "Position"],
            [
                (
                    (row.get("keys") or ["unknown"])[0],
                    str(int(row.get("clicks", 0))),
                    str(int(row.get("impressions", 0))),
                    f"{row.get('position', 0):.2f}",
                )
                for row in top
            ],
        )
    else:
        print_warning("No GSC rows returned")


@cli.command()
@click.option("--period", type=click.Choice(["7d", "30d"]), default="7d", show_default=True)
def ads(period: str) -> None:
    """Ad spend, impressions, clicks, CPA by platform."""
    data = _load_ads_metrics()
    if not data:
        print_warning("No ad metrics found. Set ADS_METRICS_PATH or ADS_METRICS_JSON.")
        return
    rows = []
    for platform, metrics in data.items():
        spend = metrics.get("spend")
        impressions = metrics.get("impressions")
        clicks = metrics.get("clicks")
        cpa = metrics.get("cpa")
        conversions = metrics.get("conversions")
        if cpa is None and conversions:
            cpa = spend / conversions if spend is not None else None
        rows.append(
            (
                str(platform),
                _format_money(spend) if spend is not None else "n/a",
                str(impressions) if impressions is not None else "n/a",
                str(clicks) if clicks is not None else "n/a",
                _format_money(cpa) if cpa is not None else "n/a",
            )
        )
    print_heading("ADS")
    print_table(f"Ads summary ({period})", ["Platform", "Spend", "Impr", "Clicks", "CPA"], rows)


@cli.command()
@click.option("--period", type=click.Choice(["30d", "90d"]), default="30d", show_default=True)
def revenue(period: str) -> None:
    """Stripe MRR, churn, new subs, revenue by product."""
    stripe_client = _stripe_client()
    if not stripe_client:
        return
    days = _parse_days(period)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    mrr = stripe_client.mrr()
    churned = stripe_client.churned_mrr(since)
    new_subs = stripe_client.new_subscriptions(since)
    total = stripe_client.revenue_total(since)
    by_product = stripe_client.revenue_by_product(since)

    print_heading("REVENUE")
    print_kv_table(
        f"Stripe ({period})",
        [
            ("MRR", _format_money(mrr)),
            ("Churned MRR", _format_money(churned)),
            ("New subs", f"{new_subs:,}"),
            ("Revenue", _format_money(total)),
        ],
    )

    if by_product:
        top_rows = sorted(by_product.items(), key=lambda item: item[1], reverse=True)
        print_table(
            "Revenue by product",
            ["Product", "Revenue", "Trend"],
            [
                (name, _format_money(amount), sparkline([amount]))
                for name, amount in top_rows
            ],
        )
    else:
        print_warning("No Stripe revenue by product")


@cli.command()
def funnel() -> None:
    """Conversion funnel from PostHog (visit -> signup -> trial -> paid)."""
    posthog = _posthog_client()
    if not posthog:
        return
    steps = os.environ.get("FUNNEL_STEPS", "$pageview,signup,trial,paid")
    events = [step.strip() for step in steps.split(",") if step.strip()]
    data = posthog.funnel(events, 30)
    result = data.get("result") or []

    print_heading("FUNNEL")
    if not result:
        print_warning("No funnel data returned")
        return

    rows = []
    prev = None
    for idx, step in enumerate(result):
        name = step.get("name") or (events[idx] if idx < len(events) else f"step {idx+1}")
        count = int(step.get("count") or 0)
        if prev in (None, 0):
            conv = "100%"
        else:
            conv = f"{(count / prev * 100):.1f}%"
        rows.append((str(name), str(count), conv))
        prev = count

    print_table("Visit -> Paid (30d)", ["Step", "Count", "Conv"], rows)


def main() -> None:
    cli(prog_name="mktg")


if __name__ == "__main__":
    main()
