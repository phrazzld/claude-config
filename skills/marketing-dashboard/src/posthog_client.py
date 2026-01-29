from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Iterable

import httpx


DEFAULT_BASE_URL = "https://app.posthog.com"


@dataclass
class PostHogClient:
    api_key: str
    project_id: str
    base_url: str = DEFAULT_BASE_URL
    timeout: float = 15.0

    @classmethod
    def from_env(cls) -> "PostHogClient":
        api_key = os.environ.get("POSTHOG_API_KEY")
        project_id = os.environ.get("POSTHOG_PROJECT_ID")
        if not api_key or not project_id:
            raise ValueError("POSTHOG_API_KEY and POSTHOG_PROJECT_ID required")
        return cls(api_key=api_key, project_id=project_id)

    def _request(self, method: str, path: str, params: dict | None = None, json: dict | None = None) -> dict:
        url = f"{self.base_url}/api/projects/{self.project_id}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.request(method, url, headers=headers, params=params, json=json)
        resp.raise_for_status()
        return resp.json()

    def trend(self, events: Iterable[str], days: int, breakdown: str | None = None) -> dict:
        payload: dict[str, Any] = {
            "events": [{"id": event} for event in events],
            "date_from": f"-{days}d",
            "interval": "day",
        }
        if breakdown:
            payload["breakdown"] = breakdown
        return self._request("POST", "/insights/trend/", json=payload)

    def funnel(self, steps: Iterable[str], days: int) -> dict:
        payload = {
            "date_from": f"-{days}d",
            "insight": "FUNNELS",
            "events": [{"id": step} for step in steps],
        }
        return self._request("POST", "/insights/funnel/", json=payload)

    def event_total(self, event: str, days: int) -> int:
        data = self.trend([event], days)
        result = data.get("result") or []
        if not result:
            return 0
        series = result[0]
        values = series.get("data") or []
        return int(sum(values))

    def top_breakdown(self, event: str, breakdown: str, days: int, limit: int = 5) -> list[tuple[str, int]]:
        data = self.trend([event], days, breakdown=breakdown)
        rows = []
        for series in data.get("result", []):
            label = str(series.get("label") or "unknown")
            values = series.get("data") or []
            count = int(sum(values))
            rows.append((label, count))
        rows.sort(key=lambda item: item[1], reverse=True)
        return rows[:limit]
