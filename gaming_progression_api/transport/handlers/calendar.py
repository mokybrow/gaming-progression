from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends

from gaming_progression_api.dependencies import UOWDep, get_current_user
from gaming_progression_api.models.service import GetFamesByMonth
from gaming_progression_api.models.users import User
from gaming_progression_api.services.calendar import CalendarService
from gaming_progression_api.services.feeds import FeedsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/calendar',
    tags=['calendar'],
)


@router.post(
    '',
)
async def get_games_by_month(
    uow: UOWDep,
    data: GetFamesByMonth,
):
    '''Получить глобальную ленту новостей для авторизованного пользователя'''
    result = await CalendarService().get_games_by_mont(uow, data)
    # print(result)
    return  result
