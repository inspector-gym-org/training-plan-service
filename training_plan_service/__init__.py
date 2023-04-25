from logging.config import dictConfig

from fastapi import FastAPI

from .config import settings
from .logging import LogConfig
from .routes import router


def build_app() -> FastAPI:
    app = FastAPI(root_path=settings.app_root_path)
    app.include_router(router)

    dictConfig(LogConfig().dict())

    return app
