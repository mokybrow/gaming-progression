from typing import List

import boto3

from fastapi import HTTPException, UploadFile, status
from markdownify import markdownify as md
from pydantic import UUID4
from sqlalchemy import exc

from gaming_progression_api.models.posts import AddPost, DeletePost, PostsResponseModel
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class PostsService:
    async def create_post(
        self,
        uow: IUnitOfWork,
        id: UUID4,
        parent_post_id: UUID4,
        text: str | None,
        file: List[UploadFile] | None,
        user_id: UUID4,
    ):
        post_text = None
        if text:
            post_text = md(text)

        async with uow:
            presence_of_wall = await uow.walls.find_one(item_id=user_id)
            '''проверяем есть ли у пользователя стена'''
            if not presence_of_wall:
                '''если стены у пользователя нет, то мы создаём её'''
                wall_type_id = await uow.wall_types.find_one(name='personal')
                await uow.walls.add_one({"item_id": user_id, "type_id": wall_type_id.id})
                await uow.commit()
                presence_of_wall = await uow.walls.find_one(item_id=user_id)

            if parent_post_id != None:
                valid_post_id_for_repost = await uow.posts.find_one(id=parent_post_id)

                if valid_post_id_for_repost:
                    try:
                        await uow.posts.add_one(
                            {
                                'id': id,
                                'user_id': user_id,
                                'wall_id': presence_of_wall.id,
                                'parent_post_id': parent_post_id,
                                'text': post_text,
                                'disabled': False,
                            }
                        )

                        await uow.commit()
                        post = await uow.posts.get_post(id=id, user_id=user_id)
                        post_data = PostsResponseModel.model_validate(post[0], from_attributes=True)

                        return post_data
                    except exc.SQLAlchemyError as ex:
                        return f'Some error {type(ex)}'

            # try:
            session = boto3.session.Session()

            s3_client = session.client(
                service_name='s3',
                endpoint_url='https://hb.vkcs.cloud',
                aws_access_key_id=settings.s3_id,
                aws_secret_access_key=settings.s3_key,
                region_name='ru-msk',
            )

            await uow.posts.add_one(
                {
                    'id': id,
                    'user_id': user_id,
                    'wall_id': presence_of_wall.id,
                    'parent_post_id': parent_post_id,
                    'text': post_text,
                    'disabled': False,
                }
            )
            if file:
                for f in file:
                    s3_client.upload_fileobj(f.file, 'mbrw', str(id) + f.filename, ExtraArgs={'ACL': 'public-read'})
                    await uow.pictures.add_one(
                        {
                            'author_id': user_id,
                            'item_id': id,
                            'picture_path': 'http://pictures.mbrw.ru/' + str(id) + f.filename,
                        }
                    )

            post = await uow.posts.get_post(id=id, user_id=user_id)
            post_data = PostsResponseModel.model_validate(post[0], from_attributes=True)
            await uow.commit()

            return post_data
            # except:
            #     return 'Some error'

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

    async def delete_post(self, uow: IUnitOfWork, post_id: UUID4, user_id: UUID4):
        async with uow:
            is_owner = await uow.posts.find_one(id=post_id, user_id=user_id)
            if is_owner:
                post_id = await uow.posts.edit_one(data={'disabled': True}, id=post_id)
                # post_id = await uow.posts.delete_one(id=post_data.post_id)
                await uow.commit()
                return f'Post with id {post_id} was deleted'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this ID not found",
        )
