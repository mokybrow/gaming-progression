from functools import lru_cache

from fastapi import APIRouter, FastAPI

from gaming_progression_api.settings import get_settings
from gaming_progression_api.transport.handlers.auth import router


def _setup_api_routers(
    api: APIRouter,
) -> None:
    api.include_router(router)


@lru_cache
def make_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
    )
    _setup_api_routers(app.router)
    return app
