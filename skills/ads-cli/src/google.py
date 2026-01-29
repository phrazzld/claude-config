"""Google Ads API wrapper using google-ads."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from google.ads.googleads.client import GoogleAdsClient


@dataclass
class GoogleAdsClientWrapper:
    """Thin wrapper for Google Ads operations."""

    developer_token: str
    client_id: str

    def auth(self) -> Dict[str, str]:
        """Validate required env vars and confirm auth wiring."""
        self._require_env()
        _ = GoogleAdsClient
        return {"platform": "google", "status": "configured"}

    def create_campaign(self, objective: str, budget: float, targeting: str) -> Dict[str, Any]:
        """Create a campaign (placeholder)."""
        self._require_env()
        return {
            "platform": "google",
            "campaign_id": "google-demo-001",
            "objective": objective,
            "budget": budget,
            "targeting": targeting,
            "status": "created",
        }

    def adjust_budget(self, campaign_id: str, amount: str) -> Dict[str, Any]:
        """Adjust budget (placeholder)."""
        self._require_env()
        return {
            "platform": "google",
            "campaign_id": campaign_id,
            "amount": amount,
            "status": "budget_updated",
        }

    def get_report(self, date_range: str) -> List[Dict[str, Any]]:
        """Return a placeholder report."""
        self._require_env()
        return [
            {
                "platform": "google",
                "date_range": date_range,
                "spend": 123.45,
                "clicks": 456,
                "conversions": 12,
                "cpa": 10.29,
                "roas": 2.7,
            }
        ]

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign (placeholder)."""
        self._require_env()
        return {"platform": "google", "campaign_id": campaign_id, "status": "paused"}

    def _require_env(self) -> None:
        if not self.developer_token or not self.client_id:
            raise ValueError(
                "Missing Google Ads env vars: GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_CLIENT_ID"
            )
