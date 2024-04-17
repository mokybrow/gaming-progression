import datetime
from pydantic import UUID4, BaseModel

from gaming_progression_api.models.users import PrivateBaseUser


class ParentPostData(BaseModel):
    id: UUID4
    user_id: UUID4
    wall_id: UUID4
    parent_post_id: UUID4 | None
    text: str
    likes_count: int
    comments_count: int
    disabled: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author_data: PrivateBaseUser | None


class PostDTO(BaseModel):
    id: UUID4
    user_id: UUID4
    wall_id: UUID4 | None
    parent_post_id: UUID4 | None
    text: str
    likes_count: int
    comments_count: int
    disabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    parent_post_data: ParentPostData | None
    author_data: PrivateBaseUser


class FeedResponseModel(BaseModel):
    Posts: PostDTO
    hasAuthorLike: int | None = None