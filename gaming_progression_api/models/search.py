from pydantic import BaseModel


class SearchModel(BaseModel):
    search_string: str
    page: int


class SearchResult(BaseModel):
    game_count: int | None
