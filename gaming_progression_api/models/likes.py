import datetime

from pydantic import UUID4, BaseModel


class LikeLogSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    type_id: UUID4
    item_id: UUID4
    value: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class LikeTypesSchema(BaseModel):
    id: UUID4
    name: str
    code: int


class AddLike(BaseModel):
    type_id: UUID4
    item_id: UUID4
    value: bool = True


class AddLikeType(BaseModel):
    name: str
    code: int
