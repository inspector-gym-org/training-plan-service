from urllib.parse import urljoin

import requests

from .models import PROPERTY_TO_ALIAS, TrainingPlan, TrainingPlansList
from .types import FilterEnum, FilterProperty


class TrainingPlansNotion:
    def __init__(
        self,
        url: str,
        timeout: int,
        integration_token: str,
        api_version: str,
        database_id: str,
    ) -> None:
        self.url = url
        self.timeout = timeout

        self.integration_token = integration_token
        self.api_version = api_version

        self.database_id = database_id

    def get_training_plans(
        self, filters: dict[FilterProperty, FilterEnum | None] | None
    ) -> list[TrainingPlan]:
        url = self.join_url(f"/v1/databases/{self.database_id}/query")
        notion_filters = []

        if filters is not None:
            notion_filters = [
                {
                    "property": PROPERTY_TO_ALIAS[property.value],
                    "select": {"equals": enum.value},
                }
                for property, enum in filters.items()
                if enum
            ]

        response = requests.post(
            url=url,
            timeout=self.timeout,
            json={"filter": {"and": notion_filters}},
            headers=self.get_headers(),
        )

        return TrainingPlansList(**response.json()).results

    def join_url(self, endpoint: str) -> str:
        return urljoin(self.url, endpoint)

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.integration_token}",
            "Notion-Version": self.api_version,
        }
