from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import ListGames, Playlists, UserLists


class CreatePlaylistsRepository(SQLAlchemyRepository):
    model = Playlists


class AddPlaylistsRepository(SQLAlchemyRepository):
    model = UserLists


class AddListGameRepository(SQLAlchemyRepository):
    model = ListGames
