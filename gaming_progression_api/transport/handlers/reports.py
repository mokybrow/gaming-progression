from typing import Annotated

from fastapi import APIRouter, Depends

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.service import CreateReportModel
from gaming_progression_api.models.users import User
from gaming_progression_api.services.reports import ReportsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/reports',
    tags=['reports'],
)


@router.post('')
async def create_report(
    uow: UOWDep,
    report: CreateReportModel,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    result = await ReportsService().create_report(uow, current_user.id, report)

    return result
