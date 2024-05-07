from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from gaming_progression_api.models.playlists import AddPlaylist, PlaylistResponseModel
from gaming_progression_api.models.schemas import PlaylistGames, Playlists, UserPlaylists, Users
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class PlaylistsService:
    async def create_new_playlist(self, uow: IUnitOfWork, playlist_data: AddPlaylist, user_id: UUID4):
        async with uow:
            get_playlist = await uow.playlists.find_one(owner_id=user_id, name=playlist_data.name)
            if get_playlist:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Youre already heave playlist with this name',
                )

            playlist_data = playlist_data.model_dump()
            playlist_data["owner_id"] = user_id
            list_id = await uow.playlists.add_one(playlist_data)
            await uow.user_playlists.add_one({"user_id": user_id, "list_id": list_id.id})
            await uow.commit()
            return f'Successfully created list with ID {list_id.id}'

    async def add_playlist(self, uow: IUnitOfWork, playlist_id: UUID4, user_id: UUID4):
        async with uow:
            check_is_owner = await uow.playlists.find_one(id=playlist_id, owner_id=user_id)
            if check_is_owner:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You cant add this list',
                )
            get_playlist = await uow.user_playlists.find_one(user_id=user_id, list_id=playlist_id)
            if get_playlist:
                await uow.user_playlists.delete_one(user_id=user_id, list_id=playlist_id)
                await uow.commit()

                return 'List was deletet from yours collection'

            await uow.user_playlists.add_one({"user_id": user_id, "list_id": playlist_id})
            await uow.commit()
            return f'Successfully created list with ID {playlist_id}'

    async def get_all_playlists(self, uow: IUnitOfWork, page: int, user_id: UUID4):
        async with uow:
            result = await uow.playlists.get_all_playlist(page=page, user_id=user_id, filter=[PlaylistGames.id != None])
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Playlists not found',
                )
            playlists = [PlaylistResponseModel.model_validate(row, from_attributes=True) for row in result]

            playlists_count = await uow.playlists.get_playlists_count(filter=[PlaylistGames.id != None])

            headers = {
                "x-playlists-count": f'{playlists_count[0][0]}',
            }
            return JSONResponse(content=jsonable_encoder(playlists), headers=headers)

    async def get_one_playlists(self, uow: IUnitOfWork, list_id: UUID4):
        async with uow:
            result = await uow.playlists.get_playlist_data(id=list_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Playlists not found',
            )
        return result[0]

    async def get_user_playlists_me(self, uow: IUnitOfWork, user_id: UUID4):
        async with uow:
            result = await uow.playlists.get_my_playlists(filter=[UserPlaylists.user_id == user_id])
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Playlists not found',
            )
        return result

    async def get_user_playlists(self, uow: IUnitOfWork, username: str, user_id: UUID4):
        async with uow:
            user = await uow.users.find_one(username=username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User Not Found',
                )
            result = await uow.playlists.get_user_playlists(user_id=user_id, filter=[UserPlaylists.user_id == user.id])
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Playlists not found',
            )
        return result

    async def add_game_to_playlist(self, uow: IUnitOfWork, list_id: UUID4, game_id: UUID4, user_id: UUID4):
        async with uow:
            check_is_owner = await uow.playlists.find_one(id=list_id, owner_id=user_id)
            if not check_is_owner:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You cant add game in this list',
                )
            found_game = await uow.playlist_games.find_one(game_id=game_id, list_id=list_id)
            if not found_game:
                result = await uow.playlist_games.add_one({"game_id": game_id, "list_id": list_id})
                await uow.commit()
                raise HTTPException(
                    status_code=status.HTTP_201_CREATED,
                    detail=f'Game {game_id} successfully added in list {list_id}',
                )
            result = await uow.playlist_games.delete_one(game_id=game_id, list_id=list_id)
            await uow.commit()

            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'{result}',
            )
