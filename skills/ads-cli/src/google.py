"""Google Ads API wrapper using google-ads v29 (API v23)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


@dataclass
class GoogleAdsClientWrapper:
    """Google Ads API client using file-based auth (~/google-ads.yaml)."""

    yaml_path: str = os.path.expanduser("~/google-ads.yaml")

    @staticmethod
    def _first_error_message(exc: GoogleAdsException) -> str:
        if getattr(exc, "failure", None) and exc.failure.errors:
            message = exc.failure.errors[0].message
            if message:
                return message
        return str(exc)

    def _client(self) -> GoogleAdsClient:
        client = GoogleAdsClient.load_from_storage(path=self.yaml_path)
        login_customer_id = (
            os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "6445466801")
            .replace("-", "")
            .strip()
        )
        client.login_customer_id = login_customer_id
        return client

    def _customer_id(self) -> str:
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "").strip()
        if not customer_id:
            raise ValueError(
                "GOOGLE_ADS_CUSTOMER_ID env var not set. "
                "Set it to your sub-account ID after account setup."
            )
        return customer_id

    @staticmethod
    def _gaql_date_range(date_range: str) -> str:
        mapping = {
            "1d": "YESTERDAY",
            "7d": "LAST_7_DAYS",
            "14d": "LAST_14_DAYS",
            "30d": "LAST_30_DAYS",
            "90d": "LAST_90_DAYS",
        }
        return mapping.get((date_range or "").lower(), "LAST_7_DAYS")

    @staticmethod
    def _micros(dollars: float) -> int:
        return int(round(float(dollars) * 1_000_000))

    @staticmethod
    def _campaign_status(status: Any) -> str:
        name = getattr(status, "name", None)
        if isinstance(name, str) and name:
            return name
        return str(status).split(".")[-1]

    @staticmethod
    def _campaign_id_from_resource(resource_name: str) -> str:
        return resource_name.rsplit("/", 1)[-1]

    @staticmethod
    def _resolve_budget_micros(amount: Any, current_amount_micros: int) -> int:
        text = str(amount).strip()
        relative_match = re.fullmatch(r"([+-])\s*(\d+(?:\.\d+)?)%", text)
        if relative_match:
            direction, percent_text = relative_match.groups()
            percent = float(percent_text) / 100.0
            factor = 1.0 + percent if direction == "+" else 1.0 - percent
            return max(0, int(round(current_amount_micros * factor)))
        return max(0, int(round(float(text) * 1_000_000)))

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def auth(self) -> Dict[str, Any]:
        """Verify auth and list accessible customers."""
        client = self._client()
        login_customer_id = (
            os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "6445466801")
            .replace("-", "")
            .strip()
        )

        try:
            customer_service = client.get_service("CustomerService")
            response = customer_service.list_accessible_customers()
        except GoogleAdsException as exc:
            raise RuntimeError(self._first_error_message(exc)) from exc

        accessible_customers = [
            resource_name.rsplit("/", 1)[-1] for resource_name in response.resource_names
        ]

        return {
            "platform": "google",
            "status": "ok",
            "login_customer_id": login_customer_id,
            "accessible_customers": accessible_customers,
        }

    def create_campaign(
        self, objective: str, budget: float, targeting: str
    ) -> Dict[str, Any]:
        """Create budget + campaign in PAUSED state. Returns IDs."""
        client = self._client()
        customer_id = self._customer_id()
        objective_lc = (objective or "").lower()

        try:
            # 1. Create shared budget
            budget_service = client.get_service("CampaignBudgetService")
            budget_operation = client.get_type("CampaignBudgetOperation")
            budget_create = budget_operation.create
            budget_create.name = f"Budget_{targeting}"
            budget_create.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
            budget_create.amount_micros = self._micros(float(budget))
            budget_create.explicitly_shared = False

            budget_response = budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_operation],
            )
            budget_resource = budget_response.results[0].resource_name

            # 2. Create campaign
            campaign_service = client.get_service("CampaignService")
            campaign_operation = client.get_type("CampaignOperation")
            campaign_create = campaign_operation.create
            campaign_create.name = f'{targeting.replace(" ", "_")}_{objective}'
            campaign_create.status = client.enums.CampaignStatusEnum.PAUSED
            campaign_create.advertising_channel_type = (
                client.enums.AdvertisingChannelTypeEnum.SEARCH
            )
            campaign_create.campaign_budget = budget_resource

            if "conversion" in objective_lc:
                campaign_create.maximize_conversions.target_cpa_micros = 0
            elif "click" in objective_lc:
                campaign_create.maximize_clicks.target_spend_amount_micros = 0
            else:
                campaign_create.manual_cpc.enhanced_cpc_enabled = False

            campaign_create.network_settings.target_google_search = True
            campaign_create.network_settings.target_search_network = True
            campaign_create.network_settings.target_content_network = False

            campaign_response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation],
            )
        except GoogleAdsException as exc:
            raise RuntimeError(self._first_error_message(exc)) from exc

        campaign_resource = campaign_response.results[0].resource_name
        campaign_id = self._campaign_id_from_resource(campaign_resource)

        return {
            "platform": "google",
            "campaign_id": campaign_id,
            "campaign_resource": campaign_resource,
            "budget_resource": budget_resource,
            "objective": objective,
            "budget_daily_usd": float(budget),
            "targeting": targeting,
            "status": "PAUSED",
        }

    def adjust_budget(self, campaign_id: str, amount: str) -> Dict[str, Any]:
        """Adjust campaign budget. amount: absolute ('35') or relative ('+20%', '-10%')."""
        client = self._client()
        customer_id = self._customer_id()
        campaign_id_str = str(campaign_id).strip()

        query = (
            "SELECT campaign.id, campaign_budget.resource_name, campaign_budget.amount_micros "
            f"FROM campaign WHERE campaign.id = {campaign_id_str}"
        )

        try:
            google_ads_service = client.get_service("GoogleAdsService")
            rows = google_ads_service.search(customer_id=customer_id, query=query)
            row = next(iter(rows), None)
            if row is None:
                raise RuntimeError(f"Campaign {campaign_id_str} not found")

            budget_resource = row.campaign_budget.resource_name
            previous_micros = int(row.campaign_budget.amount_micros)
            new_micros = self._resolve_budget_micros(amount, previous_micros)

            budget_service = client.get_service("CampaignBudgetService")
            budget_operation = client.get_type("CampaignBudgetOperation")
            budget_update = budget_operation.update
            budget_update.resource_name = budget_resource
            budget_update.amount_micros = new_micros
            budget_operation.update_mask.paths.append("amount_micros")

            budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_operation],
            )
        except GoogleAdsException as exc:
            raise RuntimeError(self._first_error_message(exc)) from exc

        return {
            "platform": "google",
            "campaign_id": campaign_id_str,
            "previous_daily_usd": previous_micros / 1_000_000,
            "new_daily_usd": new_micros / 1_000_000,
            "amount": str(amount),
            "status": "budget_updated",
        }

    def get_report(self, date_range: str) -> List[Dict[str, Any]]:
        """Return campaign performance metrics."""
        client = self._client()
        customer_id = self._customer_id()
        dr = self._gaql_date_range(date_range)

        query = f"""
            SELECT campaign.id, campaign.name, campaign.status,
                   metrics.impressions, metrics.clicks, metrics.cost_micros,
                   metrics.conversions, metrics.conversions_value
            FROM campaign
            WHERE segments.date DURING {dr}
            ORDER BY metrics.cost_micros DESC
        """

        try:
            google_ads_service = client.get_service("GoogleAdsService")
            rows = google_ads_service.search(customer_id=customer_id, query=query)
        except GoogleAdsException as exc:
            raise RuntimeError(self._first_error_message(exc)) from exc

        report: List[Dict[str, Any]] = []
        for row in rows:
            spend = float(row.metrics.cost_micros) / 1_000_000
            conversions = float(row.metrics.conversions)
            conversions_value = float(row.metrics.conversions_value)
            cpa = spend / conversions if conversions > 0 else 0.0
            roas = conversions_value / spend if spend > 0 else 0.0

            report.append({
                "platform": "google",
                "campaign_id": str(row.campaign.id),
                "campaign_name": row.campaign.name,
                "status": self._campaign_status(row.campaign.status),
                "date_range": date_range,
                "impressions": int(row.metrics.impressions),
                "clicks": int(row.metrics.clicks),
                "spend": round(spend, 2),
                "conversions": round(conversions, 2),
                "cpa": round(cpa, 2),
                "roas": round(roas, 2),
            })

        return report

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign."""
        client = self._client()
        customer_id = self._customer_id()
        campaign_id_str = str(campaign_id).strip()
        resource_name = f"customers/{customer_id}/campaigns/{campaign_id_str}"

        try:
            campaign_service = client.get_service("CampaignService")
            campaign_operation = client.get_type("CampaignOperation")
            campaign_update = campaign_operation.update
            campaign_update.resource_name = resource_name
            campaign_update.status = client.enums.CampaignStatusEnum.PAUSED
            campaign_operation.update_mask.paths.append("status")

            campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation],
            )
        except GoogleAdsException as exc:
            raise RuntimeError(self._first_error_message(exc)) from exc

        return {
            "platform": "google",
            "campaign_id": campaign_id_str,
            "status": "paused",
        }
