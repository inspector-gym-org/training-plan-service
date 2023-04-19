from fastapi import FastAPI

from .config import settings
from .routes import router


def build_app() -> FastAPI:
    app = FastAPI(root_path=settings.app_root_path)
    app.include_router(router)

    return app
