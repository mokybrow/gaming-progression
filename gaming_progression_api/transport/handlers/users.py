
from fastapi import APIRouter
from pydantic import TypeAdapter

from gaming_progression_api.dependencies import (
    UOWDep,
)
from gaming_progression_api.models.service import ServiceResponseModel
from gaming_progression_api.models.users import PrivateUser
from gaming_progression_api.services.redis import RedisTools
from gaming_progression_api.services.users import UsersService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/{username}', description='Получение профиля пользователя', response_model=PrivateUser)
async def get_user_profile(uow: UOWDep, username: str) -> PrivateUser | ServiceResponseModel:
    type_adapter = TypeAdapter(PrivateUser)

    result = await RedisTools().get_pair(key=username)
    if not result:
        user = await UsersService().get_user_profile(uow, username)
        encoded = type_adapter.dump_json(user).decode("utf-8")
        await RedisTools().set_pair(username, encoded, exp=60)
        return user

    user = type_adapter.validate_json(result)
    return user
