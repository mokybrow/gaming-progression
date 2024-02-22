from pydantic import BaseModel


class ServiceResponseModel(BaseModel):
    details: str


class SortGet(BaseModel):
    name: str
    type: str


class FilterAdd(BaseModel):
    genre: str | None
    platform: str | None
    age: str | None
    release: int | None
    limit: int | None
    sort: SortGet | None
