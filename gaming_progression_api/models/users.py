import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None
    disabled: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserCreate(BaseUser):
    password: str


class UserActivityDTO(BaseModel):
    id: UUID4
    name: str
    code: int | None


class UserActivity(BaseModel):
    activity: UserActivityDTO


class UserFavorite(BaseModel):
    id: UUID4
    user_id: UUID4
    game_id: UUID4
    created_at: datetime.datetime


class UserSubsDTO(BaseModel):
    id: UUID4


class UserFriendsDTO(BaseModel):
    id: UUID4
    username: str
    full_name: str | None


class UserFollowers(BaseModel):
    follower_data: UserFriendsDTO | None


class UserSubscriptions(BaseModel):
    sub_data: UserFriendsDTO | None


class UserListsDTO(BaseModel):
    id: UUID4
    owner_id: UUID4
    user_id: UUID4
    name: str
    about: str | None
    is_private: bool
    created_at: datetime.datetime


class User(BaseUser):
    id: UUID4
    is_verified: bool
    is_superuser: bool
    is_moderator: bool
    user_activity: list['UserActivity'] | None
    user_favorite: list['UserFavorite'] | None
    followers: list['UserFollowers'] | None
    subscriptions: list['UserSubscriptions'] | None
    lists: list['UserListsDTO'] | None


class PrivateUser(BaseModel):
    id: UUID4
    username: str
    full_name: str | None
    is_verified: bool
    is_superuser: bool
    is_moderator: bool
    user_activity: list['UserActivity'] | None
    user_favorite: list['UserFavorite'] | None
    followers: list['UserFollowers'] | None
    subscriptions: list['UserSubscriptions'] | None
    lists: list['UserListsDTO'] | None


class UserSchema(BaseUser):
    id: UUID4
    password: str
    biography: str | None
    birthdate: datetime.date | None
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
    full_name: str | None
    biography: str | None
    birthdate: datetime.date | None
    password: str | None
