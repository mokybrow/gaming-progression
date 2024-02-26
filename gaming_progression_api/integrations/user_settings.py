from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import UserMailings


class MailingRepository(SQLAlchemyRepository):
    model = UserMailings
