import datetime
from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str]
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: UUID4


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

class ChangeUserPassword(BaseModel):
    token: str
    password: str


class PatchUser(BaseModel):
    email: EmailStr
    full_name: Optional[str]
    biography: Optional[str]
    birthdate: Optional[datetime.date]