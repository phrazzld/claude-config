"""Meta Marketing API wrapper using facebook-business."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from facebook_business.api import FacebookAdsApi


@dataclass
class MetaAdsClient:
    """Thin wrapper for Meta Marketing API operations."""

    app_id: str
    app_secret: str

    def auth(self) -> Dict[str, str]:
        """Validate required env vars and confirm auth wiring."""
        self._require_env()
        _ = FacebookAdsApi
        return {"platform": "meta", "status": "configured"}

    def create_campaign(self, objective: str, budget: float, targeting: str) -> Dict[str, Any]:
        """Create a campaign (placeholder)."""
        self._require_env()
        return {
            "platform": "meta",
            "campaign_id": "meta-demo-001",
            "objective": objective,
            "budget": budget,
            "targeting": targeting,
            "status": "created",
        }

    def adjust_budget(self, campaign_id: str, amount: str) -> Dict[str, Any]:
        """Adjust budget (placeholder)."""
        self._require_env()
        return {
            "platform": "meta",
            "campaign_id": campaign_id,
            "amount": amount,
            "status": "budget_updated",
        }

    def get_report(self, date_range: str) -> List[Dict[str, Any]]:
        """Return a placeholder report."""
        self._require_env()
        return [
            {
                "platform": "meta",
                "date_range": date_range,
                "spend": 98.76,
                "clicks": 321,
                "conversions": 9,
                "cpa": 10.97,
                "roas": 2.2,
            }
        ]

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign (placeholder)."""
        self._require_env()
        return {"platform": "meta", "campaign_id": campaign_id, "status": "paused"}

    def _require_env(self) -> None:
        if not self.app_id or not self.app_secret:
            raise ValueError("Missing Meta env vars: META_APP_ID, META_APP_SECRET")
