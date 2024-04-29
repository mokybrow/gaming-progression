from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4, TypeAdapter

from gaming_progression_api.dependencies import UOWDep, get_current_user
from gaming_progression_api.models.games import (
    ChangeGameFavorite,
    ChangeGameStatus,
    GamesCountResponseModel,
    GamesResponseModel,
    RateGame,
)
from gaming_progression_api.models.service import FilterAdd, FilterCount
from gaming_progression_api.models.users import User
from gaming_progression_api.services.game_statuses import StatusesService
from gaming_progression_api.services.games import GamesService
from gaming_progression_api.services.redis import RedisTools
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/games',
    tags=['games'],
)


@router.get('/{slug}', response_model=GamesResponseModel)
async def get_game_data(uow: UOWDep, slug: str) -> GamesResponseModel:
    type_adapter = TypeAdapter(GamesResponseModel)

    result = await RedisTools().get_pair(key=slug)
    if result is None:
        result = await GamesService().get_game(uow, slug=slug)
        encoded = type_adapter.dump_json(result).decode("utf-8")

        await RedisTools().set_pair(slug, encoded, exp=40)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Game not found',
            )
        return result
    result = type_adapter.validate_json(result)
    return result


@router.post('')
async def get_games(uow: UOWDep, filters: FilterAdd):
    print(filters)
    # print(filters)
    # type_adapter_filter = TypeAdapter(FilterAdd)
    # type_adapter = TypeAdapter(list[GamesResponseModel])
    # encoded_filters = type_adapter_filter.dump_json(filters).decode("utf-8")

    # result = await RedisTools().get_pair(key=encoded_filters)
    # if not result:
    #     result = await GamesService().get_games_with_filters(uow, filters)
    #     if not result:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail='Games not found',
    #         )
    #     encoded = type_adapter.dump_json(result).decode("utf-8")

    #     await RedisTools().set_pair(encoded_filters, encoded, exp=120)
    #     return result
    # result = type_adapter.validate_json(result)
    result = await GamesService().get_games_with_filters(uow, filters)

    return result


@router.post('/count', response_model=GamesCountResponseModel)
async def get_games_count(uow: UOWDep, filters: FilterCount) -> GamesCountResponseModel:
    type_adapter_filter = TypeAdapter(FilterCount)
    type_adapter = TypeAdapter(GamesCountResponseModel)
    encoded_filters = type_adapter_filter.dump_json(filters).decode("utf-8")

    result = await RedisTools().get_pair(key=encoded_filters)
    if not result:
        result = await GamesService().get_games_count_with_filters(uow, filters)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Games not found',
            )
        encoded = type_adapter.dump_json(result).decode("utf-8")
        await RedisTools().set_pair(encoded_filters, encoded, exp=120)
        return result
    result = type_adapter.validate_json(result)

    return result


@router.post('/statuses')
async def change_game_status(
    uow: UOWDep,
    new_statuses: ChangeGameStatus,
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await StatusesService().change_status(uow, new_statuses, user_id=current_user.id)
    return result


@router.post('/favorites')
async def change_game_status(
    uow: UOWDep,
    new_favorite: ChangeGameFavorite,
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await StatusesService().change_favorite(uow, new_favorite, user_id=current_user.id)
    return result


@router.post('/rate')
async def rate_game(uow: UOWDep, rate_game: RateGame, current_user: Annotated[User, Depends(get_current_user)]):
    result = await GamesService().rate_game(uow, rate_game, user_id=current_user.id)
    return result


@router.get('/rate/{game_id}')
async def get_user_rate_game(uow: UOWDep, game_id: UUID4, current_user: Annotated[User, Depends(get_current_user)]):
    result = await GamesService().get_user_rate(uow, game_id, user_id=current_user.id)
    return result


@router.delete('/rate/{game_id}')
async def delete_game_grade(uow: UOWDep, game_id: UUID4, current_user: Annotated[User, Depends(get_current_user)]):
    result = await GamesService().delete_rate(uow, game_id=game_id, user_id=current_user.id)
    return result
