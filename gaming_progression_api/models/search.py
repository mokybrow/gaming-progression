import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class SearchModel(BaseModel):
    search_string: str
