from functools import lru_cache

from fastapi import APIRouter, FastAPI

from gaming_progression_api.settings import get_settings
from gaming_progression_api.transport.handlers.auth import router as auth_router
from gaming_progression_api.transport.handlers.games import router as games_router
from gaming_progression_api.transport.handlers.comments import router as comm_router

from fastapi.middleware.cors import CORSMiddleware


def _setup_api_routers(
    api: APIRouter,
) -> None:
    api.include_router(auth_router)
    api.include_router(games_router)
    api.include_router(comm_router)


@lru_cache
def make_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
    )
    origins = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://cultofbear.ru',
        'https://cultofbear.ru',
        'http://localhost:3000',
        'https://dudesplay.ru',
        'http://localhost:45678'
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    _setup_api_routers(app.router)
    return app
