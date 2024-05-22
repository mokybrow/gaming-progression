import datetime
from pydantic import UUID4, BaseModel


class ServiceResponseModel(BaseModel):
    details: str


class SortGet(BaseModel):
    name: str
    type: str


class FilterAdd(BaseModel):
    genre: list[int] | None
    platform: list[int] | None
    age: list[int] | None
    release: list[int] | None
    page: int
    sort: SortGet | None


class FilterCount(BaseModel):
    genre: list[str | None] | None
    platform: list[str | None] | None
    age: str | None
    release: list[int | None] | None


class ObjectTypesSchema(BaseModel):
    id: UUID4
    name: str
    code: int


class ReportSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    type: str
    content_id: UUID4
    content_type: str
    description: str | None
    created_at: datetime.datetime


class CreateReportModel(BaseModel):
    type: str
    content_id: UUID4
    content_type: str
    description: str | None


class GetFamesByMonth(BaseModel):
    date: datetime.datetime
    days: int

