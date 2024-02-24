from typing import Annotated

from fastapi import APIRouter, Depends

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.posts import AddPost, DeletePost
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
    post_data: AddPost,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    '''Создание поста должно сопровождаться привязкой его к стене'''
    result = await PostsService().create_post(uow, post_data, current_user.id)
    return result


@router.delete(
    '',
)
async def delete_post(
    uow: UOWDep,
    post_data: DeletePost,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    '''Создание поста должно сопровождаться привязкой его к стене'''
    result = await PostsService().delete_post(uow, post_data, current_user.id)
    return result
