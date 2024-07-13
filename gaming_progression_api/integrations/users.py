from gaming_progression_api.integrations.repository import SQLAlchemyRepository
from gaming_progression_api.models.schemas import Users, UserRoles


class UsersRepository(SQLAlchemyRepository):
    model = Users


class UserRolesRepository(SQLAlchemyRepository):
    model = UserRoles