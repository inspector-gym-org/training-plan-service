from pydantic import BaseModel, validator

from .types import Environment, Frequency, Goal, Level, Sex

PROPERTY_TO_ALIAS = {
    "notion_id": "id",
    "title": "Назва",
    "price": "Вартість",
    "content_url": "Посилання",
    "sex": "Стать",
    "goal": "Мета",
    "level": "Рівень Підготовки",
    "frequency": "Частота Занять",
    "environment": "Середовище",
}


class TrainingPlan(BaseModel):
    notion_id: str
    url: str

    title: str
    price: float
    content_url: str

    sex: Sex
    goal: Goal
    level: Level
    frequency: Frequency
    environment: Environment

    @validator("title", pre=True)
    def extract_title(cls, value: dict) -> str:
        if isinstance(value, dict):
            return value["title"][0]["text"]["content"]

        return value

    @validator("price", pre=True)
    def extract_price(cls, value: dict) -> float:
        if isinstance(value, dict):
            return value["number"]

        return value

    @validator("content_url", pre=True)
    def extract_url(cls, value: dict) -> str:
        if isinstance(value, dict):
            return value["url"]

        return value

    @validator("sex", "goal", "level", "frequency", "environment", pre=True)
    def extract_select(cls, value: dict) -> str:
        if isinstance(value, dict):
            return value["select"]["name"]

        return value

    def __init__(self, **data) -> None:
        if properties := data.get("properties"):
            data.pop("properties")
            data.update(properties)

        for property, alias in PROPERTY_TO_ALIAS.items():
            if i := data.get(alias):
                data.pop(alias)
                data[property] = i

        super().__init__(**data)


class TrainingPlansList(BaseModel):
    results: list[TrainingPlan]
