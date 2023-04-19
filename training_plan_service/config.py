from pydantic import BaseSettings


class Settings(BaseSettings):
    app_root_path: str

    notion_url: str
    notion_timeout: int

    notion_integration_token: str
    notion_api_version: str

    notion_database_id: str


settings = Settings()  # type: ignore[call-arg]
