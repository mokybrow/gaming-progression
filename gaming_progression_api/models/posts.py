import datetime
import uuid

from pydantic import UUID4, BaseModel

from gaming_progression_api.models.users import PrivateBaseUser


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


class GetPostModel(BaseModel):
    username: str
    offset: int

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
    text: str
    like_count: int | None
    disabled: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    users: PrivateBaseUser



class PostDTO(BaseModel):
    id: UUID4
    user_id: UUID4
    wall_id: UUID4 | None
    parent_post_id: UUID4 | None
    text: str
    like_count: int
    disabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    parent_post_data: ParentPostData | None
    users: PrivateBaseUser

class PostsResponseModel(BaseModel):
    Posts: PostDTO
    commentCount: int
    hasAuthorLike: int | None = None


class PostsCount(BaseModel):
    posts_count: int
