from datetime import datetime

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import asc, desc

from gaming_progression_api.models.games import GamesResponseModel
from gaming_progression_api.models.schemas import AgeRatings, Games, Genres, Platforms
from gaming_progression_api.models.service import FilterAdd
from gaming_progression_api.models.users import PatchUser, UserCreate
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class GamesService:
    async def get_games(self, uow: IUnitOfWork, filters: FilterAdd):
        age_rate = None
        genre = None
        platform = None
        release_start = None
        release_end = None

        if filters.genre != None:
            genre = Genres.name == filters.genre
        if filters.platform != None:
            platform = Platforms.platform_slug == filters.platform
        if filters.age != None:
            age_rate = AgeRatings.name == filters.age
        if filters.release != None:
            release_start = Games.release_date <= datetime.strptime(f'{filters.release + 1}-01-01', '%Y-%m-%d').date()
            release_end = Games.release_date >= datetime.strptime(f'{filters.release}-01-01', '%Y-%m-%d').date()
        if filters.sort != None:
            direction = desc if filters.sort.type == 'desc' else asc
            sort = direction(getattr(Games, filters.sort.name))

        async with uow:
            games = await uow.games.find_many_relation(
                genre, platform, age_rate, release_start, release_end, limit=filters.limit, sort=sort
            )

            games_response = [GamesResponseModel.model_validate(row, from_attributes=True) for row in games]

            return games_response

    async def get_game(self, uow: IUnitOfWork, **filter_by):
        async with uow:
            game = await uow.games.find_one_relation(**filter_by)
            game_response = [GamesResponseModel.model_validate(row, from_attributes=True) for row in game]

            return game_response
