from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import Users


class UsersRepository(SQLAlchemyRepository):
    model = Users
