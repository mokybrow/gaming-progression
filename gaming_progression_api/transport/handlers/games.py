from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload, selectinload, subqueryload

from gaming_progression_api.dependencies import UOWDep
from gaming_progression_api.models.games import GamesModel, GamesResponseModel
from gaming_progression_api.models.schemas import GameGenres, GamePlatforms, Games
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
async def get_games(uow: UOWDep) -> list[GamesResponseModel]:
    result = await GamesService().get_games(uow)
    return result