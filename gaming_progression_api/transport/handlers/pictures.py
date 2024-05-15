from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_superuser
from gaming_progression_api.models.posts import GetWallModel
from gaming_progression_api.models.users import User
from gaming_progression_api.models.walls import AddWallType
from gaming_progression_api.services.s3 import PicturesService
from gaming_progression_api.services.walls import WallsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/pictures',
    tags=['pictures'],
)


@router.post(
    '/add',
)
async def add_picture(uow: UOWDep, item_id: UUID4, author_id: UUID4, file: UploadFile = File(...)):
    '''Добавление картинок к посту'''

    await PicturesService().add_picture(uow, author_id, item_id, file)
