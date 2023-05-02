from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings

client = AsyncIOMotorClient(
    host=settings.mongo_host,
    port=settings.mongo_port,
    username=settings.mongo_user,
    password=settings.mongo_pass,
)

database = client[settings.mongo_database_name]
training_plans_collection = database["training_plans"]


async def create_indexes() -> None:
    await training_plans_collection.create_index("notion_id", unique=True)
