import re
from fastapi import HTTPException, status
from pydantic import UUID4

from gaming_progression_api.models.comments import AddComment, CommentsResponseModel, UserCommentsLikes
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class CommentsService:
    async def add_comment(self, uow: IUnitOfWork, comment: AddComment, user_id: UUID4):
        if comment.item_id is None and comment.parent_comment_id is None:
            return False
        comment = comment.model_dump()
        comment["user_id"] = user_id

        async with uow:
            comm = await uow.comments.add_one(comment)
            await uow.commit()
            return comm

    async def get_comments(self, uow: IUnitOfWork, item_id: UUID4):
        async with uow:
            item_comments = await uow.comments.find_one_comment(item_id=item_id, parent_comment_id=None)
            item_comments = [CommentsResponseModel.model_validate(row, from_attributes=True) for row in item_comments]
            return item_comments

    async def check_user_likes_comments(self, uow: IUnitOfWork, item_id: UUID4, user_id: UUID4):
        async with uow:
            item_comments = await uow.comments.check_user_comments_like(item_id=item_id, user_id=user_id)
            item_comments = [UserCommentsLikes.model_validate(row, from_attributes=True) for row in item_comments]
            return item_comments

    async def delete_comment(self, uow: IUnitOfWork, item_id: UUID4, user_id: UUID4):
        async with uow:
            item_comment = await uow.comments.find_one(id=item_id, user_id=user_id, deleted=False)
            if item_comment:
                item_comments = await uow.comments.edit_one(data={'deleted': True, 'text': ''}, id=item_id)
                await uow.commit()
                return f'Comment with id {item_comments} was deleted'
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't delete this comment",
            )
