from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4, TypeAdapter

from gaming_progression_api.dependencies import UOWDep, get_current_user
from gaming_progression_api.models.games import (
    ChangeGameFavorite,
    ChangeGameStatus,
    GamesCountResponseModel,
    GamesModel,
    GamesResponseModel,
    RateGame,
)
from gaming_progression_api.models.search import SearchModel
from gaming_progression_api.models.service import FilterAdd, FilterCount
from gaming_progression_api.models.users import User
from gaming_progression_api.services.game_statuses import StatusesService
from gaming_progression_api.services.games import GamesService
from gaming_progression_api.services.redis import RedisTools
from gaming_progression_api.services.search import SearchService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/search',
    tags=['search'],
)


@router.post('/games')
async def get_game_data(uow: UOWDep, search_str: SearchModel):
    # type_adapter = TypeAdapter(GamesModel)

    result = await SearchService().search_game_tsv(uow, search_str)

    return result
