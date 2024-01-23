from pydantic import UUID4, BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: UUID4
