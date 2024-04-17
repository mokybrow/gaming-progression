import datetime

from pydantic import UUID4, BaseModel


class AddComment(BaseModel):
    item_id: UUID4 | None
    parent_comment_id: UUID4 | None
    text: str
    deleted: bool = False


class CommentLikes(BaseModel):
    item_id: UUID4 | None


class CommentsSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id: UUID4 | None
    parent_comment_id: UUID4 | None
    text: str
    likes_count: int
    deleted: bool
    created_at: datetime.datetime


class UserDTO(BaseModel):
    id: UUID4
    username: str
    full_name: str | None


class LikeLog(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id: UUID4
    type_id: UUID4
    value: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ChildCommentDTO(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id: UUID4
    parent_comment_id: UUID4 | None
    created_at: datetime.datetime
    text: str
    likes_count: int
    deleted: bool
    author_data: UserDTO


class CommentsResponseModel(BaseModel):
    id: UUID4
    user_id: UUID4
    item_id: UUID4
    parent_comment_id: UUID4 | None
    created_at: datetime.datetime
    text: str
    likes_count: int
    deleted: bool
    author_data: UserDTO
    child_comment: list["ChildCommentDTO"] | None



class UserCommentsLikes(BaseModel):
    id: UUID4
    hasAuthorLike: int
