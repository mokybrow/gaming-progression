from pydantic import BaseModel


class SearchModel(BaseModel):
    search_string: str
