from pydantic import UUID4

from gaming_progression_api.models.comments import AddComment
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class CommentsService:
    async def add_comment(self, uow: IUnitOfWork, comment: AddComment, user_id: UUID4):
        if comment.item_id == None and comment.parent_comment_id == None:
            return False
        comment = comment.model_dump()
        comment["user_id"] = user_id
        async with uow:
            comm = await uow.comments.add_one(comment)
            await uow.commit()
            return comm

    async def get_comments(self, uow: IUnitOfWork, item_id: UUID4):
        async with uow:
            item_comments = await uow.comments.find_one_comment(item_id=item_id)
            return item_comments
