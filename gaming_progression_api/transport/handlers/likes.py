from typing import Annotated

from fastapi import APIRouter, Depends

from gaming_progression_api.dependencies import UOWDep, get_current_user, get_superuser
from gaming_progression_api.models.likes import AddLike, AddLikeType
from gaming_progression_api.models.users import User
from gaming_progression_api.services.likes import LikesService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/likes',
    tags=['likes'],
)


@router.post(
    '',
)
async def like_content(
    uow: UOWDep,
    like_data: AddLike,
    current_user: Annotated[User, Depends(get_current_user)],
):
    '''Поставить лайк контенту'''
    result = await LikesService().add_like_to_content(uow, like_data, current_user.id)
    return result


@router.post(
    '/add-new-type',
)
async def add_new_like_type(
    uow: UOWDep,
    like_type_data: AddLikeType,
    current_superuser: Annotated[User, Depends(get_superuser)],
):
    '''Создание нового типа лайка'''
    result = await LikesService().create_new_like_type(uow, like_type_data)
    return result
