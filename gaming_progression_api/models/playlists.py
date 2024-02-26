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
    limit: int
    offser: int


class PlaylistDTO(BaseModel):
    game_data: GameDataActivityDTO | None


class PlaylistResponseModel(BaseModel):
    id: UUID4
    name: str
    about: str | None
    created_at: datetime.datetime
    owner_data: PrivateBaseUser
    list_games: list["PlaylistDTO"]
