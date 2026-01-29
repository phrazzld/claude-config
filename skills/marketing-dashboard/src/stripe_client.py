from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
from typing import Any, Iterable

import stripe


def _to_timestamp(dt: datetime) -> int:
    return int(dt.replace(tzinfo=timezone.utc).timestamp())


def _monthly_amount(amount: int, interval: str) -> float:
    if interval == "month":
        return amount
    if interval == "year":
        return amount / 12
    if interval == "week":
        return amount * 4.345
    if interval == "day":
        return amount * 30
    return amount


@dataclass
class StripeClient:
    api_key: str

    @classmethod
    def from_env(cls) -> "StripeClient":
        api_key = os.environ.get("STRIPE_SECRET_KEY")
        if not api_key:
            raise ValueError("STRIPE_SECRET_KEY required")
        return cls(api_key=api_key)

    def _init(self) -> None:
        stripe.api_key = self.api_key

    def list_subscriptions(self, status: str, created_gte: int | None = None) -> Iterable[Any]:
        self._init()
        params: dict[str, Any] = {"status": status, "limit": 100}
        if created_gte:
            params["created"] = {"gte": created_gte}
        return stripe.Subscription.list(**params).auto_paging_iter()

    def list_invoices(self, created_gte: int) -> Iterable[Any]:
        self._init()
        return stripe.Invoice.list(
            status="paid",
            created={"gte": created_gte},
            limit=100,
            expand=["data.lines"],
        ).auto_paging_iter()

    def mrr(self) -> float:
        total = 0.0
        for sub in self.list_subscriptions(status="active"):
            for item in sub.get("items", {}).get("data", []):
                price = item.get("price") or item.get("plan") or {}
                amount = price.get("unit_amount") or price.get("amount") or 0
                interval = price.get("recurring", {}).get("interval") or price.get("interval") or "month"
                total += _monthly_amount(amount, interval)
        return total / 100

    def new_subscriptions(self, since: datetime) -> int:
        count = 0
        for _ in self.list_subscriptions(status="all", created_gte=_to_timestamp(since)):
            count += 1
        return count

    def churned_mrr(self, since: datetime) -> float:
        total = 0.0
        for sub in self.list_subscriptions(status="canceled", created_gte=_to_timestamp(since)):
            for item in sub.get("items", {}).get("data", []):
                price = item.get("price") or item.get("plan") or {}
                amount = price.get("unit_amount") or price.get("amount") or 0
                interval = price.get("recurring", {}).get("interval") or price.get("interval") or "month"
                total += _monthly_amount(amount, interval)
        return total / 100

    def revenue_by_product(self, since: datetime) -> dict[str, float]:
        totals: dict[str, float] = {}
        for invoice in self.list_invoices(created_gte=_to_timestamp(since)):
            for line in invoice.get("lines", {}).get("data", []):
                amount = line.get("amount") or 0
                price = line.get("price") or {}
                name = (
                    price.get("nickname")
                    or price.get("id")
                    or line.get("description")
                    or "unknown"
                )
                totals[name] = totals.get(name, 0.0) + (amount / 100)
        return totals

    def revenue_total(self, since: datetime) -> float:
        total = 0.0
        for invoice in self.list_invoices(created_gte=_to_timestamp(since)):
            total += invoice.get("amount_paid", 0) / 100
        return total
