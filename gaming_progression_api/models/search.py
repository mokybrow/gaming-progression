from pydantic import BaseModel


class SearchModel(BaseModel):
    search_string: str
    limit: int


class SearchResult(BaseModel):
    game_count: int | None
