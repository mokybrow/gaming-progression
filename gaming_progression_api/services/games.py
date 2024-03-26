from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import NotNullable, asc, desc

from gaming_progression_api.models.games import GamesCountResponseModel, GamesResponseModel, RateGame
from gaming_progression_api.models.schemas import Games
from gaming_progression_api.models.service import FilterAdd
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.services.validate_filters import validate_filters
from gaming_progression_api.settings import get_settings

settings = get_settings()


class GamesService:
    async def get_games_with_filters(self, uow: IUnitOfWork, filters: FilterAdd):
        true_filters = await validate_filters(filters)
        sort = None
        limit = 20
        if filters.sort is not None and filters.sort.name != 'string':
            direction = desc if filters.sort.type == 'desc' else asc
            sort = direction(getattr(Games, filters.sort.name))
            filtr = getattr(Games, filters.sort.name) != None
            true_filters.append(filtr)
            
        if filters.limit is not None and filters.limit != 0:
            limit = filters.limit 
        
        async with uow:
            games = await uow.games.find_all_games_with_filters(sort=sort, limit=limit, offset=filters.offset, filters=true_filters)
            if not games:
                return False
            games = [GamesResponseModel.model_validate(row, from_attributes=True) for row in games]
            return games

    async def get_games_count_with_filters(self, uow: IUnitOfWork, filters: FilterAdd):
        true_filters = await validate_filters(filters)

        async with uow:
            games = await uow.games.get_games_count_with_filters(filters=true_filters)
            if not games:
                return False
            return GamesCountResponseModel.model_validate({"game_count": len(games)}, from_attributes=True)


    async def get_game(self, uow: IUnitOfWork, **filter_by):
        async with uow:
            game = await uow.games.find_one_game(**filter_by)
            game_response = [GamesResponseModel.model_validate(row, from_attributes=True) for row in game]

            return game_response[0]

    async def rate_game(self, uow: IUnitOfWork, rate_game: RateGame, user_id: UUID4):
        if rate_game.grade > 10 or rate_game.grade < 1:
            raise HTTPException(
                        status_code=status.HTTP_200_OK,
                        detail='Invalid grade number',
                    )
        async with uow:
            unique_string = await uow.rates.find_one(user_id=user_id, game_id=rate_game.game_id)
            if unique_string:
                await uow.rates.edit_one(data={'grade': rate_game.grade})
                await uow.commit()
                raise HTTPException(
                        status_code=status.HTTP_200_OK,
                        detail=f'Game {rate_game.game_id} grade changed to {rate_game.grade}',
                    )
            rate_game = rate_game.model_dump()
            rate_game['user_id'] = user_id
            await uow.rates.add_one(rate_game)
            await uow.commit()
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'Game {rate_game['game_id']} added grade {rate_game['grade']}',
            )
    
    async def get_user_rate(self, uow: IUnitOfWork, game_id: RateGame, user_id: UUID4):
        async with uow:
            unique_string = await uow.rates.find_one(user_id=user_id, game_id=game_id)
            if unique_string:
                return unique_string.grade
            return 0
        
    async def delete_rate(self, uow: IUnitOfWork,  game_id: UUID4, user_id: UUID4):

        async with uow:
            unique_string = await uow.rates.find_one(user_id=user_id, game_id=game_id)
            if unique_string:
                await uow.rates.delete_one(user_id=user_id, game_id=game_id)
                await uow.commit()
                raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail=f'Game {game_id} review deleted successfully',
                )