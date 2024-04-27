from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import exc

from gaming_progression_api.models.posts import AddPost, DeletePost, GetWallModel, PostsCount, PostsResponseModel
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings
from markdownify import markdownify as md

settings = get_settings()


class PostsService:
    async def create_post(self, uow: IUnitOfWork, post_data: AddPost, user_id: UUID4):
        post_text = md(post_data.text)

        async with uow:
            presence_of_wall = await uow.walls.find_one(item_id=user_id)
            '''проверяем есть ли у пользователя стена'''
            if not presence_of_wall:
                '''если стены у пользователя нет, то мы создаём её'''
                wall_type_id = await uow.wall_types.find_one(name='personal')
                await uow.walls.add_one({"item_id": user_id, "type_id": wall_type_id.id})
                await uow.commit()
                presence_of_wall = await uow.walls.find_one(item_id=user_id)

            if post_data.parent_post_id is not None:
                valid_post_id_for_repost = await uow.posts.find_one(id=post_data.parent_post_id)

                if valid_post_id_for_repost:
                    post_data = post_data.model_dump()
                    post_data['wall_id'] = presence_of_wall.id
                    post_data['user_id'] = user_id
                    post_data['text'] = post_text
                    try:
                        repost = await uow.posts.add_one(post_data)
                        await uow.commit()
                        return repost
                    except exc.SQLAlchemyError as ex:
                        return f'Some error {type(ex)}'
            

            post_data = post_data.model_dump()
            post_data['wall_id'] = presence_of_wall.id
            post_data['user_id'] = user_id
            post_data['text'] = post_text
            print(post_text)
            try:
                post = await uow.posts.add_one(post_data)
                await uow.commit()
                return post
            except:
                return 'Some error'

    async def get_user_posts(self, uow: IUnitOfWork, params: GetWallModel):
        async with uow:
            user = await uow.users.find_one(username=params.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            wall_id = await uow.walls.find_one(item_id=user.id)
            if not wall_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )

            posts = await uow.posts.get_user_posts(offset=params.offset, wall_id=wall_id.id)
            if not posts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )

            wall = [PostsResponseModel.model_validate(row, from_attributes=True) for row in posts]
            return wall

    async def get_auth_user_posts(self, uow: IUnitOfWork, params: GetWallModel, user_id: UUID4):
        async with uow:
            user = await uow.users.find_one(username=params.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            wall_id = await uow.walls.find_one(item_id=user.id)
            if not wall_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )

            posts = await uow.posts.get_user_wall(wall_id=wall_id.id, user_id=user_id, offset=params.offset)
            if not posts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )

            wall = [PostsResponseModel.model_validate(row, from_attributes=True) for row in posts]
            return wall

    async def get_post(self, uow: IUnitOfWork, id: UUID4, user_id: UUID4):
        async with uow:
            post = await uow.posts.get_post(id=id, user_id=user_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )

            wall = PostsResponseModel.model_validate(post[0], from_attributes=True)
            return wall

    async def get_posts_count(self, uow: IUnitOfWork, username: str):
        async with uow:
            user = await uow.users.find_one(username=username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            wall_id = await uow.walls.find_one(item_id=user.id)
            if not wall_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )

            posts = await uow.posts.get_posts_count(wall_id=wall_id.id)
            if not posts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )
            return PostsCount.model_validate(posts[0], from_attributes=True)

    async def delete_post(self, uow: IUnitOfWork, post_data: DeletePost, user_id: UUID4):
        async with uow:
            is_owner = await uow.posts.find_one(id=post_data.post_id, user_id=user_id)
            if is_owner:
                post_id = await uow.posts.delete_one(id=post_data.post_id)
                await uow.commit()
                return f'Post with id {post_id} was deleted'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this ID not found",
        )
