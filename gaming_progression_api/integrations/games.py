from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import Games


class GamesRepository(SQLAlchemyRepository):
    model = Games
