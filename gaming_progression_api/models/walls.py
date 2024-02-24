
from pydantic import UUID4, BaseModel


class WallsSchema(BaseModel):
    id: UUID4
    type_id: UUID4
    item_id: UUID4


class WallTypesSchema(BaseModel):
    id: UUID4
    name: str
    code: int


class AddWall(BaseModel):
    wall_id: UUID4
    parent_post_id: UUID4 | None
    text: str
    disabled: bool = False


class AddWallType(BaseModel):
    name: str
    code: int
