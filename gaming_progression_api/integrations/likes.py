from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import LikeLog, LikeTypes


class LikesRepository(SQLAlchemyRepository):
    model = LikeLog


class LikeTypesRepository(SQLAlchemyRepository):
    model = LikeTypes
