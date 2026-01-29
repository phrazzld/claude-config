from __future__ import annotations

import os
from typing import Any, Iterable

import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def load_credentials():
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path:
        return service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    creds, _ = google.auth.default(scopes=SCOPES)
    return creds


def build_service():
    creds = load_credentials()
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def query_search_analytics(
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: Iterable[str] | None = None,
    row_limit: int = 250,
) -> list[dict[str, Any]]:
    service = build_service()
    body: dict[str, Any] = {
        "startDate": start_date,
        "endDate": end_date,
        "rowLimit": row_limit,
    }
    if dimensions:
        body["dimensions"] = list(dimensions)
    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    return response.get("rows", [])
