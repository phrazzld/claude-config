"""Google Places API v1 Text Search client."""

from __future__ import annotations

import httpx

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = ",".join([
    "places.displayName",
    "places.formattedAddress",
    "places.nationalPhoneNumber",
    "places.websiteUri",
    "places.rating",
    "places.userRatingCount",
    "places.businessStatus",
    "places.id",
])

NATIONAL_CHAINS = frozenset({
    "starbucks", "mcdonald", "dunkin", "subway", "chipotle", "panera",
    "chick-fil-a", "domino", "pizza hut", "papa john", "taco bell",
    "burger king", "wendy", "sonic", "popeyes", "kfc", "five guys",
    "shake shack", "in-n-out", "whataburger", "raising cane",
    "cookout", "applebee", "chili's", "olive garden", "red lobster",
    "ihop", "denny's", "waffle house", "cracker barrel",
    "buffalo wild wings", "hooters", "pf chang", "cheesecake factory",
    "jersey mike", "jimmy john", "firehouse subs", "blaze pizza",
    "mod pizza", "sweetgreen", "wingstop", "crumbl", "dutch bros",
})


def search(query: str, api_key: str, limit: int = 20) -> list[dict]:
    """Fetch up to `limit` places matching `query` via Google Places API v1."""
    results: list[dict] = []
    page_token: str | None = None

    with httpx.Client(timeout=30) as client:
        while len(results) < limit:
            body: dict = {
                "textQuery": query,
                "maxResultCount": min(20, limit - len(results)),
            }
            if page_token:
                body["pageToken"] = page_token

            resp = client.post(
                PLACES_URL,
                headers={
                    "X-Goog-Api-Key": api_key,
                    "X-Goog-FieldMask": FIELD_MASK,
                    "Content-Type": "application/json",
                },
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()

            places = data.get("places", [])
            results.extend(places)

            page_token = data.get("nextPageToken")
            if not page_token or not places:
                break

    return results[:limit]


def is_chain(name: str, website: str) -> bool:
    """Return True if the business looks like a national chain to skip."""
    name_lower = name.lower()
    if any(chain in name_lower for chain in NATIONAL_CHAINS):
        return True
    # Multi-location indicator in URL
    if website and "/locations/" in website.lower():
        return True
    return False
