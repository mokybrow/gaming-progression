from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4, TypeAdapter

from gaming_progression_api.dependencies import UOWDep, get_current_user
from gaming_progression_api.models.service import ServiceResponseModel
from gaming_progression_api.models.user_settings import MailingSettingsResponseModel
from gaming_progression_api.models.users import PrivateUser, User
from gaming_progression_api.services.redis import RedisTools
from gaming_progression_api.services.users import UsersService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/{username}', description='Получение профиля пользователя', response_model=PrivateUser)
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


@router.post('/follow/{user_id}')
async def follow_on_user(
    uow: UOWDep,
    user_id: UUID4,
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await UsersService().follow_on_user(uow, current_user.id, user_id)
    return result


@router.get('/settings/mailing')
async def mailing_settings(
    uow: UOWDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[MailingSettingsResponseModel]:
    result = await UsersService().get_user_mailing_settings(uow, current_user.id)
    return result


@router.patch('/settings/mailing')
async def mailing_settings(
    uow: UOWDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await UsersService().patch_user_mailing_settings(uow, current_user.id)
    return result
