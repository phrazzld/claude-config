---
name: ads-cli
description: Unified ad platform CLI + Python clients for Google Ads, Meta, and TikTok. Use when building or running commands for auth, campaign creation, budget changes, reporting, or pausing campaigns. Google Ads is fully wired with real API calls. Meta/TikTok are stubs.
effort: high
---

# Ads CLI

Manage paid ads across Google/Meta/TikTok via one CLI and unified client.

## Auth

Google Ads: file-based auth via `~/google-ads.yaml`. No env vars for credentials.

Required env vars (set in `~/.secrets`):
```bash
export GOOGLE_ADS_LOGIN_CUSTOMER_ID=6445466801   # Canonical MCC (phaedrus@mistystep.io)
export GOOGLE_ADS_CUSTOMER_ID=<sub_account_id>   # Set after account creation unblocked
```

Meta / TikTok (stubs — not yet implemented):
```bash
export META_APP_ID=...
export META_APP_SECRET=...
export TIKTOK_ACCESS_TOKEN=...
```

## Quick Start

```bash
cd ~/.claude/skills/ads-cli

# Verify auth + list accessible customers
python cli.py auth --platform google

# Report (requires GOOGLE_ADS_CUSTOMER_ID)
python cli.py report --platforms google --date-range 7d --format table

# Create campaign (PAUSED, requires GOOGLE_ADS_CUSTOMER_ID)
python cli.py create-campaign --platform google --objective conversions --budget 35 --targeting "AI consulting"

# Adjust budget (+20%, absolute, or negative)
python cli.py adjust-budget --platform google --campaign-id <id> --amount "+20%"

# Pause campaign
python cli.py pause --platform google --campaign-id <id>
```

## Account Context (Misty Step)

- **Canonical MCC**: `6445466801` (phaedrus@mistystep.io)
- **Config**: `~/google-ads.yaml`
- **Blocker**: MCC has a policy flag blocking sub-account creation via API.
  Resolve at ads.google.com before creating campaigns.
- **MCC `2673211237`**: Secondary, leave untouched.
- **`customers/8507948813`**: Defunct (permission denied), ignore.

## First Campaign

When account is unblocked:
```bash
python cli.py create-campaign --platform google \
  --objective conversions --budget 35 \
  --targeting "GOOG_Search_AIConsulting_LeadGen_2026Q1"
```

Full campaign spec in `~/Development/misty-step/marketing/channels/google-ads/README.md`.

## Structure

- `cli.py` — Click commands
- `src/google.py` — Real Google Ads API v23 implementation
- `src/meta.py`, `src/tiktok.py` — Stubs
- `src/unified.py` — Routes by platform

## Extend

Add new platform wrapper with `auth`, `create_campaign`, `adjust_budget`, `get_report`, `pause_campaign`.
Register it in `UnifiedAdsClient`.

Strategy reference: `~/.claude/skills/paid-ads/SKILL.md`
