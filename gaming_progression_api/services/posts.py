from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import exc

from gaming_progression_api.models.posts import AddPost, DeletePost
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class PostsService:
    async def create_post(self, uow: IUnitOfWork, post_data: AddPost, user_id: UUID4):
        async with uow:
            presence_of_wall = await uow.walls.find_one(item_id=user_id)
            '''проверяем есть ли у ползователя стена'''
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
                    try:
                        post_id = await uow.posts.add_one(post_data)
                        await uow.commit()
                        return f'Repost with id {post_id} was created'
                    except exc.SQLAlchemyError as ex:
                        return f'Some error {type(ex)}'

            post_data = post_data.model_dump()
            post_data['wall_id'] = presence_of_wall.id
            post_data['user_id'] = user_id
            try:
                post_id = await uow.posts.add_one(post_data)
                await uow.commit()
                return f'Post with id {post_id} was created'
            except:
                return 'Some error'

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
