import datetime
from typing import List
import uuid

from pydantic import UUID4, BaseModel

from gaming_progression_api.models.users import PrivateBaseUser
from gaming_progression_api.models.walls import PicturesDTO


class PostsSchema(BaseModel):
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


class AddPost(BaseModel):
    id: UUID4 = uuid.uuid4()
    parent_post_id: UUID4 | None
    text: str
    disabled: bool = False


class GetWallModel(BaseModel):
    username: str
    user_id: UUID4 | None
    page: int


class GetPostData(BaseModel):
    id: UUID4
    user_id: UUID4 | None


class DeletePost(BaseModel):
    post_id: UUID4


class ParentPostData(BaseModel):
    id: UUID4
    user_id: UUID4
    wall_id: UUID4
    parent_post_id: UUID4 | None
    text: str | None
    likes_count: int | None
    comments_count: int
    disabled: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author_data: PrivateBaseUser | None
    pictures: List[PicturesDTO] | None


class PostDTO(BaseModel):
    id: UUID4
    user_id: UUID4
    wall_id: UUID4 | None
    parent_post_id: UUID4 | None
    text: str | None
    likes_count: int
    comments_count: int
    disabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    parent_post_data: ParentPostData | None
    author_data: PrivateBaseUser
    pictures: List[PicturesDTO] | None


class PostsResponseModel(BaseModel):
    Posts: PostDTO
    hasAuthorLike: int | None = None


class PostsCount(BaseModel):
    posts_count: int
