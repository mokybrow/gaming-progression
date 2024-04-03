from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.posts import AddPost, DeletePost, GetPostData, GetPostModel
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


@router.post(
    '/get',
)
async def get_user_posts(
    uow: UOWDep,
    params: GetPostModel,
):
    '''Получаем посты со стены пользователя'''
    result = await PostsService().get_user_posts(uow, params=params)
    return result


@router.post(
    '/get/auth',
)
async def get_auth_user_posts(
    uow: UOWDep,
    params: GetPostModel,
    current_user: Annotated[User, Depends(get_current_active_user)],

):
    '''Получаем посты со стены пользователя'''
    result = await PostsService().get_auth_user_posts(uow, params=params, user_id=current_user.id)
    return result


@router.post(
    '/post',
)
async def get_post(
    uow: UOWDep,
    params: GetPostData
):
    '''Получаем пост и комметарии к нему'''
    result = await PostsService().get_post(uow, id=params.id, user_id=params.user_id)
    return result



@router.get(
    '/count/{username}',
)
async def get_posts_count(
    uow: UOWDep,
    username: str,

):
    '''Получаем посты со стены пользователя'''
    result = await PostsService().get_posts_count(uow, username=username)
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
