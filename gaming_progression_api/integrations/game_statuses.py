from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import ActivityTypes, UserActivity, UserFavorite


class StatusesRepository(SQLAlchemyRepository):
    model = UserActivity


class FavoriteRepository(SQLAlchemyRepository):
    model = UserFavorite


class ActivityTypesRepository(SQLAlchemyRepository):
    model = ActivityTypes
