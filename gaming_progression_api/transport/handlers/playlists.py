from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.playlists import (
    AddGameToPlaylist,
    AddPlaylist,
    GetPlaylists,
    GetUserPlaylists,
    PlaylistDTO,
    PlaylistResponseModel,
)
from gaming_progression_api.models.users import User
from gaming_progression_api.services.playlists import PlaylistsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/playlists',
    tags=['playlists'],
)


@router.post(
    '/create',
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
async def add_playlist_to_my_collection(
    uow: UOWDep,
    list_id: UUID4,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    '''Добавить плейлист к себе в коллекцию'''
    result = await PlaylistsService().add_playlist(uow, list_id, current_user.id)
    return result


@router.post('/get/all', response_model=list[PlaylistResponseModel])
async def get_playlists(uow: UOWDep, playlist_data: GetPlaylists):
    '''Получить список всех плейлистов'''
    result = await PlaylistsService().get_all_playlists(uow, page=playlist_data.page, user_id=playlist_data.user_id)
    return result


@router.get(
    '/{list_id}',
)
async def get_playlist_data(
    uow: UOWDep,
    list_id: UUID4,
) -> PlaylistDTO:
    '''Получить информацию о списке и играх в нём'''
    result = await PlaylistsService().get_one_playlists(uow, list_id)
    return result


@router.get(
    '/user/me',
)
async def get_my_playlists(
    uow: UOWDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> list[PlaylistDTO]:
    '''Получить свои списки'''
    result = await PlaylistsService().get_user_playlists_me(uow, current_user.id)
    return result


@router.post(
    '/user/get',
)
async def get_user_playlists(uow: UOWDep, playlist_data: GetUserPlaylists) -> list[PlaylistResponseModel]:
    '''Получить списки пользователя'''
    print(playlist_data)
    result = await PlaylistsService().get_user_playlists(uow, playlist_data.username, playlist_data.user_id)
    return result


@router.post(
    '/add/game',
)
async def add_game_to_list(
    uow: UOWDep,
    playlist_data: AddGameToPlaylist,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> PlaylistResponseModel:
    '''Добавить игру в список'''
    result = await PlaylistsService().add_game_to_playlist(
        uow, playlist_data.list_id, playlist_data.game_id, current_user.id
    )
    return result
