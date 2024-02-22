from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4, TypeAdapter
from redis.asyncio import Redis

from gaming_progression_api.dependencies import UOWDep, get_current_active_user, get_current_user
from gaming_progression_api.models.games import ChangeGameFavorite, ChangeGameStatus, GamesResponseModel, RateGame
from gaming_progression_api.models.posts import AddPost
from gaming_progression_api.models.service import FilterAdd
from gaming_progression_api.models.users import User
from gaming_progression_api.services.game_statuses import StatusesService
from gaming_progression_api.services.games import GamesService
from gaming_progression_api.services.posts import PostsService
from gaming_progression_api.services.redis import RedisTools
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/posts',
    tags=['posts'],
)


@router.post(
    '',
)
async def add_new_post(
    uow: UOWDep,
    post_data: AddPost,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    result = await PostsService().create_post(uow, post_data, current_user.id)
    return result
