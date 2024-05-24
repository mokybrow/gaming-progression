from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user, get_current_user
from gaming_progression_api.models.posts import AddPost, DeletePost, PostsResponseModel
from gaming_progression_api.models.users import User
from gaming_progression_api.services.posts import PostsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/posts',
    tags=['posts'],
)


@router.post(
    '',
)
async def add_new_post(
    uow: UOWDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    id: UUID4 = Form(...),
    parent_post_id: UUID4 = Form(None),
    text: str = Form(None),
    file: List[UploadFile] = File(None),
):
    '''Создание поста должно сопровождаться привязкой его к стене'''
    result = await PostsService().create_post(uow, id, parent_post_id, text, file, current_user.id)

    return result


@router.get(
    '',
)
async def get_post(uow: UOWDep, id: UUID4, user_id: UUID4 | None = None):
    '''Получаем пост и комметарии к нему'''
    result = await PostsService().get_post(uow, id=id, user_id=user_id)
    return result


@router.delete(
    '/{post_id}',
)
async def delete_post(
    uow: UOWDep,
    post_id: UUID4,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    '''Удаление поста происходит путём его деактивации'''
    result = await PostsService().delete_post(uow, post_id, current_user.id)
    return result
