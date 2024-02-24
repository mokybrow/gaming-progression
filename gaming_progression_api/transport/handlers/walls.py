from typing import Annotated

from fastapi import APIRouter, Depends

from gaming_progression_api.dependencies import UOWDep, get_superuser
from gaming_progression_api.models.users import User
from gaming_progression_api.models.walls import AddWallType
from gaming_progression_api.services.walls import WallsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/walls',
    tags=['walls'],
)


@router.post(
    '/add-new-type',
)
async def add_new_wall_type(
    uow: UOWDep,
    wall_type_data: AddWallType,
    current_superuser: Annotated[User, Depends(get_superuser)],
):
    '''Создание нового типа стены'''
    result = await WallsService().create_new_wall_type(uow, wall_type_data)
    return result
