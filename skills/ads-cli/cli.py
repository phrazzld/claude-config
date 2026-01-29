#!/usr/bin/env python3
"""Ads CLI entry point."""

from __future__ import annotations

import csv
import json
from typing import Any, Dict, List

import click
from rich.console import Console
from rich.table import Table

from src.unified import UnifiedAdsClient


def _client() -> UnifiedAdsClient:
    return UnifiedAdsClient.from_env()


def _parse_platforms(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@click.group()
def ads() -> None:
    """Unified ad platform CLI."""


@ads.command("auth")
@click.option("--platform", required=True, type=click.Choice(["google", "meta", "tiktok"]))
def auth_cmd(platform: str) -> None:
    """Validate auth env vars for a platform."""
    result = _client().auth(platform)
    click.echo(json.dumps(result, indent=2))


@ads.command("create-campaign")
@click.option("--platform", required=True, type=click.Choice(["google", "meta", "tiktok"]))
@click.option("--objective", required=True, type=str)
@click.option("--budget", required=True, type=float)
@click.option("--targeting", required=True, type=str)
def create_campaign_cmd(platform: str, objective: str, budget: float, targeting: str) -> None:
    """Create a campaign."""
    result = _client().create_campaign(platform, objective, budget, targeting)
    click.echo(json.dumps(result, indent=2))


@ads.command("adjust-budget")
@click.option("--platform", required=True, type=click.Choice(["google", "meta", "tiktok"]))
@click.option("--campaign-id", required=True, type=str)
@click.option("--amount", required=True, type=str)
def adjust_budget_cmd(platform: str, campaign_id: str, amount: str) -> None:
    """Adjust a campaign budget."""
    result = _client().adjust_budget(platform, campaign_id, amount)
    click.echo(json.dumps(result, indent=2))


@ads.command("report")
@click.option("--platforms", required=True, type=str, help="Comma-separated list")
@click.option("--date-range", default="7d", type=str)
@click.option(
    "--format",
    "output_format",
    default="table",
    type=click.Choice(["table", "csv", "json"]),
)
def report_cmd(platforms: str, date_range: str, output_format: str) -> None:
    """Generate a report across platforms."""
    rows = _client().get_report(_parse_platforms(platforms), date_range)
    if output_format == "json":
        click.echo(json.dumps(rows, indent=2))
        return
    if output_format == "csv":
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(click.get_text_stream("stdout"), fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        return
    _render_table(rows)


@ads.command("pause")
@click.option("--platform", required=True, type=click.Choice(["google", "meta", "tiktok"]))
@click.option("--campaign-id", required=True, type=str)
def pause_cmd(platform: str, campaign_id: str) -> None:
    """Pause a campaign."""
    result = _client().pause_campaign(platform, campaign_id)
    click.echo(json.dumps(result, indent=2))


def _render_table(rows: List[Dict[str, Any]]) -> None:
    console = Console()
    table = Table(title="Ads Report")
    columns = ["platform", "date_range", "spend", "clicks", "conversions", "cpa", "roas"]
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*(str(row.get(col, "")) for col in columns))
    console.print(table)


if __name__ == "__main__":
    ads()
