from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.playlists import AddPlaylist, PlaylistResponseModel
from gaming_progression_api.models.users import User
from gaming_progression_api.services.playlists import PlaylistsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/playlists',
    tags=['playlists'],
)


@router.post(
    '',
)
async def create_new_playlist(
    uow: UOWDep,
    playlist_data: AddPlaylist,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    '''Создать новый список с играми'''
    result = await PlaylistsService().create_new_playlist(uow, playlist_data, current_user.id)
    return result


@router.post(
    '/{list_id}',
)
async def add_playlist_to_my(
    uow: UOWDep,
    list_id: UUID4,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    '''Создать новый список с играми'''
    result = await PlaylistsService().add_playlist(uow, list_id, current_user.id)
    return result


@router.get(
    '',
)
async def get_playlists(uow: UOWDep, limit: int, offset: int):
    '''Получить информацию о списке и играх в нём'''
    result = await PlaylistsService().get_all_playlists(uow, limit=limit, offset=offset)
    return result


@router.get(
    '/{list_id}',
)
async def get_playlist_data(
    uow: UOWDep,
    list_id: UUID4,
) -> PlaylistResponseModel:
    '''Получить информацию о списке и играх в нём'''
    result = await PlaylistsService().get_one_playlists(uow, list_id)
    return result


@router.post(
    '/{list_id}/games/{game_id}',
)
async def add_game_to_list(
    uow: UOWDep,
    list_id: UUID4,
    game_id: UUID4,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> PlaylistResponseModel:
    '''Получить информацию о списке и играх в нём'''
    result = await PlaylistsService().add_game_to_playlist(uow, list_id, game_id, current_user.id)
    return result
