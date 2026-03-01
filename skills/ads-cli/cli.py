#!/usr/bin/env python3
"""Ads CLI entry point."""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List

import click
from rich.console import Console
from rich.table import Table

from src.unified import UnifiedAdsClient


def _load_secrets() -> None:
    """Load ~/.secrets into env if not already set. Handles 'export KEY=val' format."""
    p = Path.home() / ".secrets"
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Strip leading 'export ' if present
        if line.startswith("export "):
            line = line[7:]
        if "=" in line:
            k, _, v = line.partition("=")
            # Strip surrounding quotes from value
            v = v.strip().strip("\"'")
            os.environ.setdefault(k.strip(), v)


_load_secrets()


def _client() -> UnifiedAdsClient:
    return UnifiedAdsClient.from_env()


def _parse_platforms(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@click.group()
@click.option("--product", default=None, envvar="ADS_PRODUCT", help="Product name context")
@click.pass_context
def ads(ctx: click.Context, product: str | None) -> None:
    """Unified ad platform CLI."""
    ctx.ensure_object(dict)
    ctx.obj["product"] = product


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


# ---------------------------------------------------------------------------
# Prospect command group
# ---------------------------------------------------------------------------

@ads.group("prospect")
@click.pass_context
def prospect_group(ctx: click.Context) -> None:
    """Prospect discovery pipeline for Nashville SMBs."""
    if not ctx.obj.get("product"):
        raise click.UsageError("--product is required for prospect commands")


def _prospects_base(product: str) -> Path:
    return Path.home() / "Development" / product / "marketing" / "prospects"


@prospect_group.command("discover")
@click.option("--query", required=True, help='e.g. "restaurants"')
@click.option("--city", default="Nashville TN", show_default=True)
@click.option("--limit", default=20, show_default=True, help="Max results to fetch")
@click.option("--min-reviews", default=10, show_default=True)
@click.option("--max-rating", default=5.0, show_default=True, help="Exclude above this rating (5.0 = no filter)")
@click.pass_context
def discover_cmd(
    ctx: click.Context,
    query: str,
    city: str,
    limit: int,
    min_reviews: int,
    max_rating: float,
) -> None:
    """Discover Nashville SMB prospects via Google Places API."""
    from src.places import is_chain, search
    from src.prospect import Prospect, load_csv, merge, save_csv

    api_key = os.environ.get("GOOGLE_PLACES_API_KEY") or os.environ.get("GOOGLE_PLACE_API_KEY")
    if not api_key:
        raise click.ClickException("GOOGLE_PLACES_API_KEY (or GOOGLE_PLACE_API_KEY) not set")

    product = ctx.obj["product"]
    base = _prospects_base(product)
    csv_path = str(base / f"{product}.csv")

    full_query = f"{query} in {city}"
    click.echo(f"Searching: {full_query!r} (limit={limit})")

    raw = search(full_query, api_key, limit=limit)
    click.echo(f"  Got {len(raw)} raw results from Places API")

    qualified: list[Prospect] = []
    for place in raw:
        name = place.get("displayName", {}).get("text", "")
        website = place.get("websiteUri", "")
        status = place.get("businessStatus", "")
        rating = place.get("rating")
        review_count = place.get("userRatingCount", 0)

        # Pre-filter (fast, no agent needed)
        if not website:
            continue
        if status != "OPERATIONAL":
            continue
        if review_count < min_reviews:
            continue
        if rating is not None and rating > max_rating:
            continue
        if is_chain(name, website):
            continue

        qualified.append(
            Prospect(
                name=name,
                address=place.get("formattedAddress", ""),
                phone=place.get("nationalPhoneNumber"),
                website=website,
                rating=rating,
                review_count=review_count,
                place_id=place["id"],
            )
        )

    click.echo(f"  {len(qualified)} passed qualification filter")

    existing = load_csv(csv_path)
    merged = merge(existing, qualified)
    save_csv(merged, csv_path)

    added = len(merged) - len(existing)
    click.echo(f"  +{added} new | {len(merged)} total → {csv_path}")


@prospect_group.command("assess")
@click.option("--limit", default=5, show_default=True, help="Max prospects to assess")
@click.option("--parallel", default=3, show_default=True, help="Concurrent assessments")
@click.option(
    "--agent",
    default="gemini",
    show_default=True,
    type=click.Choice(["gemini", "claude", "codex"]),
    help="LLM agent for analysis",
)
@click.pass_context
def assess_cmd(
    ctx: click.Context,
    limit: int,
    parallel: int,
    agent: str,
) -> None:
    """Assess discovered prospects (scrape + LLM analysis)."""
    from src.prospect import STATUS_DISCOVERED, load_csv, save_csv

    product = ctx.obj["product"]
    base = _prospects_base(product)
    csv_path = str(base / f"{product}.csv")
    profiles_dir = base / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    prospects = load_csv(csv_path)
    to_assess = [p for p in prospects if p.status == STATUS_DISCOVERED][:limit]

    if not to_assess:
        click.echo("No discovered prospects to assess.")
        return

    click.echo(f"Assessing {len(to_assess)} prospect(s) with agent={agent!r}")

    def assess_one(idx: int, p: object) -> object:
        from src.prospect import STATUS_ASSESSED

        click.echo(f"  [{idx+1}/{len(to_assess)}] {p.name} — {p.website}")

        # Step 1: Scrape with agent-browser
        scraped = _scrape(p.website)

        # Step 2: Analyze with LLM
        prompt = _build_assess_prompt(p, scraped)
        raw = _dispatch_assess(agent, prompt)

        # Step 3: Parse and persist
        profile_path = profiles_dir / f"{p.slug}.json"
        try:
            profile = _extract_json(raw)
            profile["_meta"] = {
                "name": p.name,
                "website": p.website,
                "address": p.address,
                "place_id": p.place_id,
            }
            profile_path.write_text(json.dumps(profile, indent=2))
            p.profile_path = str(profile_path)
            p.status = STATUS_ASSESSED
            click.echo(f"    score={profile.get('prospect_score', '?')} → {profile_path.name}")
        except Exception as e:
            click.echo(f"    [warn] parse failed: {e}", err=True)

        return p

    # Run in parallel
    updated: dict[str, object] = {}
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {pool.submit(assess_one, i, p): p.place_id for i, p in enumerate(to_assess)}
        for fut in as_completed(futures):
            result = fut.result()
            updated[result.place_id] = result

    # Merge results back and save
    for i, p in enumerate(prospects):
        if p.place_id in updated:
            prospects[i] = updated[p.place_id]

    save_csv(prospects, csv_path)
    click.echo(f"Done. {len(updated)} assessed → {csv_path}")


def _scrape(url: str) -> str:
    """Fetch homepage text via agent-browser. Returns empty string on failure."""
    try:
        result = subprocess.run(
            ["npx", "agent-browser", "navigate", url, "get", "text", "--json"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return result.stdout[:8000]  # bounded
        click.echo(f"    [warn] agent-browser exit {result.returncode}", err=True)
    except subprocess.TimeoutExpired:
        click.echo("    [warn] agent-browser timed out", err=True)
    except FileNotFoundError:
        click.echo("    [warn] agent-browser not found (npx)", err=True)
    except Exception as e:
        click.echo(f"    [warn] scrape error: {e}", err=True)
    return ""


def _build_assess_prompt(prospect: object, scraped: str) -> str:
    content_section = f"\n=== WEBSITE CONTENT ===\n{scraped}\n=== END ===" if scraped else "\n(Website could not be scraped — analyze from URL and business name only)"
    return f"""You are assessing a Nashville SMB as a prospect for Misty Step, a web design agency that rebuilds websites as outreach.

Business: {prospect.name}
Website: {prospect.website}
Location: {prospect.address}
Rating: {prospect.rating} ({prospect.review_count} reviews)
{content_section}

Analyze their online presence and return ONLY valid JSON — no markdown, no explanation:

{{
  "brand": {{"colors": ["#hex"], "fonts": [], "aesthetic_score": 1}},
  "copy_tone": "description of voice/tone",
  "services": ["service1"],
  "team": ["name/role"],
  "contact": {{"phone": "", "email": "", "address": ""}},
  "weaknesses": ["specific observed problems"],
  "prospect_score": 8,
  "recommendation": "what we would build for them"
}}

prospect_score guide (1-10):
- 8-10: Poor website, clear opportunity, real established business
- 5-7: Mediocre website, some opportunity
- 1-4: Website already good, low opportunity

Return ONLY the JSON object."""


def _dispatch_assess(agent: str, prompt: str) -> str:
    """Invoke LLM agent and return raw output."""
    try:
        match agent:
            case "gemini":
                result = subprocess.run(
                    ["gemini", prompt],
                    capture_output=True, text=True, timeout=180,
                )
            case "claude":
                result = subprocess.run(
                    ["claude", "-p", prompt],
                    capture_output=True, text=True, timeout=180,
                )
            case "codex":
                result = subprocess.run(
                    ["codex", "--yolo", "--search", "-q", prompt],
                    capture_output=True, text=True, timeout=180,
                )
            case _:
                raise ValueError(f"Unknown agent: {agent}")

        if result.returncode != 0 and result.stderr:
            click.echo(f"    [warn] agent stderr: {result.stderr[:200]}", err=True)
        return result.stdout
    except subprocess.TimeoutExpired:
        click.echo("    [warn] agent timed out", err=True)
        return ""
    except FileNotFoundError as e:
        click.echo(f"    [warn] agent not found: {e}", err=True)
        return ""


def _extract_json(text: str) -> dict:
    """Parse JSON from LLM response, tolerating surrounding text."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip markdown fences
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    # Find first JSON object
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    raise ValueError("No JSON found in agent response")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

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
