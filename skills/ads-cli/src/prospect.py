"""Prospect dataclass and persistent CSV state management."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

STATUS_DISCOVERED = "discovered"
STATUS_ASSESSED = "assessed"
STATUS_APPROVED = "approved"
STATUS_BUILT = "built"
STATUS_SENT = "sent"

CSV_FIELDS = [
    "place_id", "slug", "name", "address", "phone", "website",
    "rating", "review_count", "status", "profile_path", "vercel_url",
]


@dataclass
class Prospect:
    name: str
    address: str
    phone: str | None
    website: str
    rating: float | None
    review_count: int
    place_id: str
    slug: str = field(default="")
    status: str = STATUS_DISCOVERED
    profile_path: str | None = None
    vercel_url: str | None = None

    def __post_init__(self) -> None:
        if not self.slug:
            self.slug = _slug_from_url(self.website)

    def to_row(self) -> dict:
        return {
            "place_id": self.place_id,
            "slug": self.slug,
            "name": self.name,
            "address": self.address,
            "phone": self.phone or "",
            "website": self.website,
            "rating": str(self.rating) if self.rating is not None else "",
            "review_count": str(self.review_count),
            "status": self.status,
            "profile_path": self.profile_path or "",
            "vercel_url": self.vercel_url or "",
        }

    @classmethod
    def from_row(cls, row: dict) -> "Prospect":
        return cls(
            place_id=row["place_id"],
            slug=row.get("slug", ""),
            name=row["name"],
            address=row["address"],
            phone=row.get("phone") or None,
            website=row["website"],
            rating=float(row["rating"]) if row.get("rating") else None,
            review_count=int(row.get("review_count") or 0),
            status=row.get("status", STATUS_DISCOVERED),
            profile_path=row.get("profile_path") or None,
            vercel_url=row.get("vercel_url") or None,
        )


def _slug_from_url(url: str) -> str:
    try:
        normalized = url if "://" in url else f"https://{url}"
        host = urlparse(normalized).netloc.lstrip("www.")
        return re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-") or "unknown"
    except Exception:
        return "unknown"


def load_csv(path: str) -> list[Prospect]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return [Prospect.from_row(row) for row in csv.DictReader(f)]


def save_csv(prospects: list[Prospect], path: str) -> None:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(p.to_row() for p in prospects)


def merge(existing: list[Prospect], new: list[Prospect]) -> list[Prospect]:
    """Merge prospect lists by place_id; existing rows win (preserves status)."""
    by_id = {p.place_id: p for p in existing}
    for p in new:
        if p.place_id not in by_id:
            by_id[p.place_id] = p
    return list(by_id.values())
