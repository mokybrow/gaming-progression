from functools import lru_cache

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gaming_progression_api.settings import get_settings
from gaming_progression_api.transport.handlers.auth import router as auth_router
from gaming_progression_api.transport.handlers.comments import router as comm_router
from gaming_progression_api.transport.handlers.feeds import router as feeds_router
from gaming_progression_api.transport.handlers.games import router as games_router
from gaming_progression_api.transport.handlers.likes import router as likes_router
from gaming_progression_api.transport.handlers.playlists import router as playlists_router
from gaming_progression_api.transport.handlers.posts import router as posts_router
from gaming_progression_api.transport.handlers.search import router as search_router
from gaming_progression_api.transport.handlers.users import router as users_router
from gaming_progression_api.transport.handlers.walls import router as walls_router
from gaming_progression_api.transport.handlers.reports import router as reports_router
from gaming_progression_api.transport.handlers.pictures import router as pic_router


def _setup_api_routers(
    api: APIRouter,
) -> None:
    api.include_router(auth_router)
    api.include_router(games_router)
    api.include_router(comm_router)
    api.include_router(posts_router)
    api.include_router(walls_router)
    api.include_router(likes_router)
    api.include_router(users_router)
    api.include_router(playlists_router)
    api.include_router(feeds_router)
    api.include_router(search_router)
    api.include_router(reports_router)
    api.include_router(pic_router)


@lru_cache
def make_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
    )
    origins = [
        'http://localhost:3000',
        'http://localhost:3000/feed',
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['x-post-count', ' x-comment-count', 'x-games-count', 'x-playlists-count'],
    )
    _setup_api_routers(app.router)
    return app
