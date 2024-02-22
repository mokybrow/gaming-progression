from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.comments import AddComment
from gaming_progression_api.models.users import User
from gaming_progression_api.services.comments import CommentsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(prefix='/comments', tags=['comments'])


@router.post(
    '',
)
async def add_new_comment(
    uow: UOWDep,
    comment: AddComment,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    result = await CommentsService().add_comment(uow, comment, current_user.id)
    return result


@router.get(
    '/{id}',
)
async def get_comments(uow: UOWDep, id: UUID4):
    result = await CommentsService().get_comments(uow, id)
    return result


@router.delete(
    '/{id}',
)
async def delete_comment(uow: UOWDep, id: UUID4, current_user: Annotated[User, Depends(get_current_active_user)]):
    result = await CommentsService().delete_comment(uow, id, current_user.id)
    return result