from pydantic import UUID4, BaseModel


class ServiceResponseModel(BaseModel):
    details: str


class SortGet(BaseModel):
    name: str
    type: str


class FilterAdd(BaseModel):
    genre: list[str | None] | None
    platform: list[str | None] | None
    age: str | None
    release: list[int | None] | None
    limit: int | None
    offset: int | None
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
