from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload, selectinload, subqueryload

from gaming_progression_api.dependencies import UOWDep, get_current_user
from gaming_progression_api.models.games import ChangeGameStatus, GamesModel, GamesResponseModel
from gaming_progression_api.models.schemas import GameGenres, GamePlatforms, Games, Genres, Platforms
from gaming_progression_api.models.service import FilterAdd
from gaming_progression_api.models.users import User
from gaming_progression_api.services.game_statuses import StatusesService
from gaming_progression_api.services.games import GamesService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/games',
    tags=['games'],
)


@router.get('/{slug}', response_model=list[GamesResponseModel])
async def get_game_data(uow: UOWDep, slug: str) -> list[GamesResponseModel]:
    result = await GamesService().get_game(uow, slug=slug)
    return result


@router.post('', response_model=list[GamesResponseModel])
async def get_games(uow: UOWDep, filters: FilterAdd) -> list[GamesResponseModel]:
    result = await GamesService().get_games(uow, filters)
    return result


@router.post('/statuses')
async def change_game_status(
    uow: UOWDep, new_statuses: ChangeGameStatus, current_user: Annotated[User, Depends(get_current_user)]
):
    result = await StatusesService().change_status(uow, new_statuses, user_id=current_user.id)
    return result
