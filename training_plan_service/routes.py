from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .database import training_plans_collection
from .logging_route import LoggingRoute
from .models import TrainingPlan
from .notion import get_all_training_plans
from .types import Environment, FilterEnum, FilterProperty, Frequency, Goal, Level, Sex

router = APIRouter(prefix="/plans", tags=["training-plans"], route_class=LoggingRoute)


@router.get("/")
async def get_training_plans(
    sex: Sex | None = None,
    goal: Goal | None = None,
    level: Level | None = None,
    frequency: Frequency | None = None,
    environment: Environment | None = None,
) -> list[TrainingPlan]:
    return await training_plans_collection.find(
        jsonable_encoder(
            {
                FilterProperty.SEX: sex,
                FilterProperty.GOAL: goal,
                FilterProperty.LEVEL: level,
                FilterProperty.FREQUENCY: frequency,
                FilterProperty.ENVIRONMENT: environment,
            },
            exclude_none=True,
        )
    ).to_list(length=None)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def fetch_training_plans() -> None:
    training_plans = await get_all_training_plans()

    for plan in training_plans:
        await training_plans_collection.update_one(
            {"notion_id": plan.notion_id}, {"$set": jsonable_encoder(plan)}, upsert=True
        )


@router.get("/{training_plan_id}/")
async def get_training_plan(training_plan_id: str) -> TrainingPlan:
    if training_plan := await training_plans_collection.find_one(
        {"notion_id": training_plan_id}
    ):
        return training_plan

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/property/{property}/")
async def get_property_values(
    property: FilterProperty,
    sex: Sex | None = None,
    goal: Goal | None = None,
    level: Level | None = None,
    frequency: Frequency | None = None,
    environment: Environment | None = None,
) -> list[FilterEnum]:
    return await training_plans_collection.distinct(
        property.value,
        jsonable_encoder(
            {
                FilterProperty.SEX: sex,
                FilterProperty.GOAL: goal,
                FilterProperty.LEVEL: level,
                FilterProperty.FREQUENCY: frequency,
                FilterProperty.ENVIRONMENT: environment,
            },
            exclude_none=True,
        ),
    )
