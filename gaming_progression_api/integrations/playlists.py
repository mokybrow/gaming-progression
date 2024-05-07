from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import PlaylistGames, Playlists, UserPlaylists


class CreatePlaylistsRepository(SQLAlchemyRepository):
    model = Playlists


class AddPlaylistsRepository(SQLAlchemyRepository):
    model = UserPlaylists


class AddListGameRepository(SQLAlchemyRepository):
    model = PlaylistGames
