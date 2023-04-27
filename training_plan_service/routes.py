from enum import Enum
from uuid import UUID

from fastapi import APIRouter

from .config import settings
from .logging_route import LoggingRoute
from .models import TrainingPlan
from .notion import TrainingPlansNotion
from .types import Environment, FilterProperty, Frequency, Goal, Level, Sex

router = APIRouter(
    tags=["training-plans"],
    route_class=LoggingRoute,
)

database = TrainingPlansNotion(
    url=settings.notion_url,
    timeout=settings.notion_timeout,
    integration_token=settings.notion_integration_token,
    api_version=settings.notion_api_version,
    database_id=settings.notion_database_id,
)


@router.get("/")
async def get_training_plans(
    sex: Sex | None = None,
    goal: Goal | None = None,
    level: Level | None = None,
    frequency: Frequency | None = None,
    environment: Environment | None = None,
) -> list[TrainingPlan]:
    return database.get_training_plans(
        filters={
            FilterProperty.SEX: sex,
            FilterProperty.GOAL: goal,
            FilterProperty.LEVEL: level,
            FilterProperty.FREQUENCY: frequency,
            FilterProperty.ENVIRONMENT: environment,
        }
    )


@router.get("/{training_plan_id}")
async def get_training_plan(training_plan_id: UUID) -> TrainingPlan:
    return database.get_training_plan(training_plan_id)


@router.get("/existing-property-values/")
async def get_existing_property_values(
    property: FilterProperty,
    sex: Sex | None = None,
    goal: Goal | None = None,
    level: Level | None = None,
    frequency: Frequency | None = None,
    environment: Environment | None = None,
) -> set[Enum]:
    plans = database.get_training_plans(
        filters={
            FilterProperty.SEX: sex,
            FilterProperty.GOAL: goal,
            FilterProperty.LEVEL: level,
            FilterProperty.FREQUENCY: frequency,
            FilterProperty.ENVIRONMENT: environment,
        }
    )

    attrs = [getattr(plan, property.value) for plan in plans]
    return set(attrs)
