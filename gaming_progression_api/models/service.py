import datetime

from typing import Optional

from pydantic import BaseModel

from gaming_progression_api.models.schemas import Genres, Platforms


class ServiceResponseModel(BaseModel):
    details: str


class SortGet(BaseModel):
    name: str
    type: str


class FilterAdd(BaseModel):
    genre: Optional[str]
    platform: Optional[str]
    age: Optional[str]
    release: Optional[int]
    limit: Optional[int]
    sort: Optional[SortGet]
