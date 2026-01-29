"""TikTok Business API wrapper (placeholder)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TikTokAdsClient:
    """Placeholder wrapper for TikTok Business API operations."""

    access_token: str

    def auth(self) -> Dict[str, str]:
        """Validate required env vars and confirm auth wiring."""
        self._require_env()
        return {"platform": "tiktok", "status": "configured"}

    def create_campaign(self, objective: str, budget: float, targeting: str) -> Dict[str, Any]:
        """Create a campaign (placeholder)."""
        self._require_env()
        return {
            "platform": "tiktok",
            "campaign_id": "tiktok-demo-001",
            "objective": objective,
            "budget": budget,
            "targeting": targeting,
            "status": "created",
        }

    def adjust_budget(self, campaign_id: str, amount: str) -> Dict[str, Any]:
        """Adjust budget (placeholder)."""
        self._require_env()
        return {
            "platform": "tiktok",
            "campaign_id": campaign_id,
            "amount": amount,
            "status": "budget_updated",
        }

    def get_report(self, date_range: str) -> List[Dict[str, Any]]:
        """Return a placeholder report."""
        self._require_env()
        return [
            {
                "platform": "tiktok",
                "date_range": date_range,
                "spend": 65.0,
                "clicks": 210,
                "conversions": 5,
                "cpa": 13.0,
                "roas": 1.8,
            }
        ]

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign (placeholder)."""
        self._require_env()
        return {"platform": "tiktok", "campaign_id": campaign_id, "status": "paused"}

    def _require_env(self) -> None:
        if not self.access_token:
            raise ValueError("Missing TikTok env var: TIKTOK_ACCESS_TOKEN")
