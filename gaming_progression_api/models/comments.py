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

class UserDTO(BaseModel):
    id: UUID4
    username: str
    full_name: str | None

class ChildCommentDTO(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id:UUID4
    created_at: datetime.datetime
    text: str
    like_count: int
    deleted: bool
    author_info: UserDTO


class CommentsResponseModel(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id:UUID4
    created_at: datetime.datetime
    text: str
    like_count: int
    deleted: bool
    author_info: UserDTO
    child_comment: list["ChildCommentDTO"] 