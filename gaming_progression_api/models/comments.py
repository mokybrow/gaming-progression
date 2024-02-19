import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class AddComment(BaseModel):
    item_id: Optional[UUID4]
    parent_comment_id: Optional[UUID4]
    text: str
    deleted: bool = False


class CommentsSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id: Optional[UUID4]
    parent_comment_id: Optional[UUID4]
    text: str
    like_count: int
    deleted: bool
    created_at: datetime.datetime