from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import Games, GameReviews


class GamesRepository(SQLAlchemyRepository):
    model = Games


class GamesReviewsRepository(SQLAlchemyRepository):
    model = GameReviews
