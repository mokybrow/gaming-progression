from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user, get_current_user
from gaming_progression_api.models.comments import AddComment, CommentLikes, CommentsSchema
from gaming_progression_api.models.users import User
from gaming_progression_api.services.comments import CommentsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(prefix='/comments', tags=['comments'])


@router.get(
    '',
)
async def get_comments(uow: UOWDep, id: UUID4, user_id: UUID4 | None = None):
    result = await CommentsService().get_comments(uow, id, user_id)
    return result


@router.post('', response_model=CommentsSchema)
async def add_new_comment(
    uow: UOWDep,
    comment: AddComment,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    result = await CommentsService().add_comment(uow, comment, current_user.id)
    return result


@router.post(
    '/likes',
)
async def get_comments(
    uow: UOWDep,
    comment: CommentLikes,
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await CommentsService().check_user_likes_comments(uow, comment.item_id, current_user.id)
    return result


@router.delete(
    '/{id}',
)
async def delete_comment(uow: UOWDep, id: UUID4, current_user: Annotated[User, Depends(get_current_active_user)]):
    result = await CommentsService().delete_comment(uow, id, current_user.id)
    return result
