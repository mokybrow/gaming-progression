from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import Pictures


class PicturesRepository(SQLAlchemyRepository):
    model = Pictures
