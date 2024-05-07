from typing import Annotated

from fastapi import APIRouter, Depends

from gaming_progression_api.dependencies import UOWDep, get_current_user
from gaming_progression_api.models.users import User
from gaming_progression_api.services.feeds import FeedsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/feeds',
    tags=['feeds'],
)


@router.get(
    '',
)
async def get_global_feed_for_auth(
    uow: UOWDep,
    page: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    '''Получить глобальную ленту новостей для авторизованного пользователя'''
    result = await FeedsService().get_global_feed_for_auth(uow, page, current_user.id)
    return result
