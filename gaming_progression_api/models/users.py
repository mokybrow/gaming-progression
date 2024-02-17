import datetime

from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str]
    disabled: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserCreate(BaseUser):
    password: str


class UserActivityDTO(BaseModel):
    id: UUID4
    name: str
    code: Optional[int]


class UserActivity(BaseModel):
    activity: UserActivityDTO


class UserFavorite(BaseModel):
    id: UUID4
    user_id: UUID4
    game_id: UUID4
    created_at: datetime.datetime

class UserSubsDTO(BaseModel):
    id: UUID4

class UserFriendsDTO(BaseUser):
    id: UUID4


class UserFriends(BaseModel):
    follower_data: Optional[UserFriendsDTO]


class UserFriends2(BaseModel):
    sub_data: Optional[UserFriendsDTO]

class UserListsDTO(BaseModel):
    id: UUID4
    owner_id: UUID4
    user_id: UUID4
    name: str
    about: Optional[str]
    is_private: bool
    created_at: datetime.datetime


class User(BaseUser):
    id: UUID4
    is_verified: bool
    is_superuser: bool
    is_moderator: bool
    user_activity: Optional[list['UserActivity']] 
    user_favorite: Optional[list['UserFavorite']]
    followers: Optional[list['UserFriends']]
    subscriptions: Optional[list['UserFriends2']]
    lists: Optional[list['UserListsDTO']]


class UserSchema(BaseUser):
    id: UUID4
    password: str
    biography: Optional[str]
    birthdate: Optional[datetime.date]
    is_verified: bool
    is_superuser: bool
    is_moderator: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ChangeUserPassword(BaseModel):
    token: str
    password: str


class PatchUser(BaseModel):
    email: EmailStr
    full_name: Optional[str]
    biography: Optional[str]
    birthdate: Optional[datetime.date]
    password: Optional[str]
