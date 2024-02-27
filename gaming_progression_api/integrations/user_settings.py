from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import MailingTypes, UserMailings


class MailingRepository(SQLAlchemyRepository):
    model = UserMailings


class MailingTypesRepository(SQLAlchemyRepository):
    model = MailingTypes
