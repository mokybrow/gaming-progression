from pydantic import UUID4, BaseModel


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
    offset: int | None
    sort: SortGet | None


class ObjectTypesSchema(BaseModel):
    id: UUID4
    name: str
    code: int
