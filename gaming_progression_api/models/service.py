from typing import List

from pydantic import UUID4, BaseModel


class ServiceResponseModel(BaseModel):
    details: str


class SortGet(BaseModel):
    name: str
    type: str


class FilterAdd(BaseModel):
    genre: List[str | None] | None
    platform: List[str | None] | None
    age: str | None
    release: List[int | None] | None
    limit: int | None
    offset: int | None
    sort: SortGet | None


class ObjectTypesSchema(BaseModel):
    id: UUID4
    name: str
    code: int
