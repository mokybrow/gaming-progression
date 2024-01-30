from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4

from gaming_progression_api.dependencies import (
    UOWDep,
    access_token_expires,
    get_current_user,
    reset_token_expires,
    verify_token_expires,
)
from gaming_progression_api.models.games import SearchGame
from gaming_progression_api.models.schemas import Games

from gaming_progression_api.services.games import GamesService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/games',
    tags=['games'],
)


@router.post(
    '',
)
async def get_games(
    uow: UOWDep,
    id: UUID4
):
    result = await GamesService().get_game(uow, id=id)
    return result
