import datetime

from pydantic import UUID4, BaseModel


class AddComment(BaseModel):
    item_id: UUID4 | None
    parent_comment_id: UUID4 | None
    text: str
    deleted: bool = False


class CommentsSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id: UUID4 | None
    parent_comment_id: UUID4 | None
    text: str
    like_count: int
    deleted: bool
    created_at: datetime.datetime
