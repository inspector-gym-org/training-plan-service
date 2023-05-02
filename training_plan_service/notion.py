import httpx

from .config import settings
from .models import TrainingPlan, TrainingPlansList


async def get_all_training_plans() -> list[TrainingPlan]:
    url = settings.notion_url + f"/v1/databases/{settings.notion_database_id}/query"
    headers = {
        "Authorization": f"Bearer {settings.notion_integration_token}",
        "Notion-Version": settings.notion_api_version,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url, timeout=settings.notion_timeout, headers=headers
        )

    return TrainingPlansList(**response.json()).results
