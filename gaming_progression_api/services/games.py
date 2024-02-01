from fastapi import HTTPException, status
from pydantic import UUID4

from gaming_progression_api.models.games import GamesResponseModel
from gaming_progression_api.models.users import PatchUser, UserCreate
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class GamesService:
    async def get_games(self, uow: IUnitOfWork, **filter_by):
        async with uow:
            games = await uow.games.find_many_relation(**filter_by)

            games_response = [GamesResponseModel.model_validate(row, from_attributes=True) for row in games]

            return games_response

    async def get_game(self, uow: IUnitOfWork, **filter_by):
        async with uow:
            game = await uow.games.find_one_relation(**filter_by)
            game_response = [GamesResponseModel.model_validate(row, from_attributes=True) for row in game]

            return game_response
