import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserCreate(BaseUser):
    password: str


class GameDataActivityDTO(BaseModel):
    id: UUID4
    title: str
    description: str | None
    release_date: datetime.datetime | None
    cover: str | None


class UserActivityDTO(BaseModel):
    id: UUID4
    name: str
    code: int


class UserActivity(BaseModel):
    game_data: GameDataActivityDTO | None
    activity_data: UserActivityDTO | None


class UserFavorite(BaseModel):
    game_data: GameDataActivityDTO | None


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
    name: str
    about: str | None
    is_private: bool
    created_at: datetime.datetime


class UserLists(BaseModel):
    playlists: UserListsDTO | None


class User(BaseUser):
    id: UUID4
    is_verified: bool
    is_superuser: bool
    is_moderator: bool
    user_activity: list['UserActivity'] | None
    user_favorite: list['UserFavorite'] | None
    followers: list['UserFollowers'] | None
    subscriptions: list['UserSubscriptions'] | None
    lists: list['UserLists'] | None


class PrivateBaseUser(BaseModel):
    id: UUID4
    username: str
    full_name: str | None


class PrivateUser(PrivateBaseUser):
    user_activity: list['UserActivity'] | None
    user_favorite: list['UserFavorite'] | None
    followers: list['UserFollowers'] | None
    subscriptions: list['UserSubscriptions'] | None
    lists: list['UserLists'] | None


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


class UserMailingsSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    mailing_id: UUID4
    created_at: datetime.datetime
