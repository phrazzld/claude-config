"""Unified ads client routing to platform-specific clients."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping

from .google import GoogleAdsClientWrapper
from .meta import MetaAdsClient
from .tiktok import TikTokAdsClient


@dataclass
class UnifiedAdsClient:
    """Route ads operations to per-platform clients."""

    google: GoogleAdsClientWrapper | None
    meta: MetaAdsClient | None
    tiktok: TikTokAdsClient | None

    @classmethod
    def from_env(cls) -> "UnifiedAdsClient":
        """Build clients from env vars."""
        return cls(
            google=GoogleAdsClientWrapper(
                developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", ""),
                client_id=os.getenv("GOOGLE_ADS_CLIENT_ID", ""),
            ),
            meta=MetaAdsClient(
                app_id=os.getenv("META_APP_ID", ""),
                app_secret=os.getenv("META_APP_SECRET", ""),
            ),
            tiktok=TikTokAdsClient(access_token=os.getenv("TIKTOK_ACCESS_TOKEN", "")),
        )

    def auth(self, platform: str) -> Dict[str, Any]:
        return self._client(platform).auth()

    def create_campaign(
        self, platform: str, objective: str, budget: float, targeting: str
    ) -> Dict[str, Any]:
        return self._client(platform).create_campaign(objective, budget, targeting)

    def adjust_budget(self, platform: str, campaign_id: str, amount: str) -> Dict[str, Any]:
        return self._client(platform).adjust_budget(campaign_id, amount)

    def get_report(self, platforms: Iterable[str], date_range: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for platform in platforms:
            rows.extend(self._client(platform).get_report(date_range))
        return rows

    def pause_campaign(self, platform: str, campaign_id: str) -> Dict[str, Any]:
        return self._client(platform).pause_campaign(campaign_id)

    def _client(self, platform: str):
        key = platform.strip().lower()
        clients: Mapping[str, Any] = {
            "google": self.google,
            "meta": self.meta,
            "tiktok": self.tiktok,
        }
        client = clients.get(key)
        if client is None:
            raise ValueError(f"Unsupported or unconfigured platform: {platform}")
        return client
