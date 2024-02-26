from fastapi import HTTPException, status
from pydantic import UUID4

from gaming_progression_api.models.playlists import AddPlaylist
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class PlaylistsService:
    async def create_new_playlist(self, uow: IUnitOfWork, playlist_data: AddPlaylist, user_id: UUID4):
        async with uow:
            get_playlist = await uow.playlists.find_one(owner_id=user_id, name=playlist_data.name)
            if get_playlist:
                return 'Youre already heave playlist with this name'

            playlist_data = playlist_data.model_dump()
            playlist_data["owner_id"] = user_id
            list_id = await uow.playlists.add_one(playlist_data)
            await uow.add_playlists.add_one({"user_id": user_id, "list_id": list_id})
            await uow.commit()
            return f'Successfully created list with ID {list_id}'

    async def add_playlist(self, uow: IUnitOfWork, playlist_id: UUID4, user_id: UUID4):
        async with uow:
            get_playlist = await uow.add_playlists.find_one(user_id=user_id, list_id=playlist_id)
            if get_playlist:
                await uow.add_playlists.delete_one(user_id=user_id, list_id=playlist_id)
                await uow.commit()

                return 'List was deletet from yours collection'

            await uow.add_playlists.add_one({"user_id": user_id, "list_id": playlist_id})
            await uow.commit()
            return f'Successfully created list with ID {playlist_id}'

    async def get_all_playlists(self, uow: IUnitOfWork, limit: int | None = None, offset: int | None = None):
        async with uow:
            result = await uow.playlists.find_all(limit, offset)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Playlists not found',
            )
        return result

    async def get_one_playlists(self, uow: IUnitOfWork, list_id: UUID4):
        async with uow:
            result = await uow.playlists.get_playlist_data(id=list_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Playlists not found',
            )
        return result[0]

    async def add_game_to_playlist(self, uow: IUnitOfWork, list_id: UUID4, game_id: UUID4, user_id: UUID4):
        async with uow:
            check_is_owner = await uow.playlists.find_one(id=list_id, owner_id=user_id)
            if not check_is_owner:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You cant add game in this list',
                )
            found_game = await uow.list_games.find_one(game_id=game_id, list_id=list_id)
            if not found_game:
                result = await uow.list_games.add_one({"game_id": game_id, "list_id": list_id})
                await uow.commit()
                raise HTTPException(
                    status_code=status.HTTP_201_CREATED,
                    detail=f'Game {game_id} successfully added in list {list_id}',
                )
            result = await uow.list_games.delete_one(game_id=game_id, list_id=list_id)
            await uow.commit()

            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'{result}',
            )
