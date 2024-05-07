import datetime

from pydantic import UUID4, BaseModel

from gaming_progression_api.models.users import GameDataActivityDTO, PrivateBaseUser


class PlaylistsSchema(BaseModel):
    id: UUID4
    owner_id: UUID4
    name: str
    about: str | None
    is_private: bool
    created_at: datetime.datetime


class UserListsSchema(BaseModel):
    id: UUID4
    list_id: UUID4
    user_id: UUID4
    created_at: datetime.datetime


class AddGameListSchema(BaseModel):
    id: UUID4
    game_id: UUID4
    list_id: UUID4
    created_at: datetime.datetime


class AddPlaylist(BaseModel):
    name: str
    about: str | None = None
    is_private: bool = False


class GetPlaylists(BaseModel):
    page: int
    user_id: UUID4 | None


class GetUserPlaylists(BaseModel):
    username: str
    user_id: UUID4 | None


class AddGameToPlaylist(BaseModel):
    list_id: UUID4
    game_id: UUID4


class GamesPlaylistDTO(BaseModel):
    game_data: GameDataActivityDTO


class PlaylistDTO(BaseModel):
    id: UUID4
    owner_id: UUID4
    name: str
    about: str | None
    created_at: datetime.datetime
    owner_data: PrivateBaseUser
    list_games: list["GamesPlaylistDTO"]


class PlaylistResponseModel(BaseModel):
    Playlists: PlaylistDTO
    addedPlaylist: int | None = None
