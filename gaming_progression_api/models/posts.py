import datetime
import uuid

from pydantic import UUID4, BaseModel


class PostsSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    wall_id: UUID4 | None
    parent_post_id: UUID4 | None
    text: str
    like_count: int
    disabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AddPost(BaseModel):
    id: UUID4 = uuid.uuid4()
    parent_post_id: UUID4 | None
    text: str
    disabled: bool = False


class DeletePost(BaseModel):
    post_id: UUID4
