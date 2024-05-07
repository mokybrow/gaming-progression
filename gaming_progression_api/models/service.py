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
