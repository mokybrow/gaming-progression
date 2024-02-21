import datetime

from ast import List
from typing import Any, Optional

from pydantic import UUID4, BaseModel, ConfigDict


class GamesModel(BaseModel):
    id: UUID4
    title: str
    cover: Optional[str]
    description: Optional[str]
    slug: str
    release_date: Optional[datetime.datetime]
    playtime: Optional[int]
    completed_count: Optional[int]
    wishlist_count: Optional[int]
    favorite_count: Optional[int]
    avg_rate: Optional[float]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GenreDTO(BaseModel):
    id: UUID4
    name: str
    name_ru: Optional[str]
    code: Optional[int]


class Genre(BaseModel):
    genre: GenreDTO


class PlatformDTO(BaseModel):
    id: UUID4
    platform_name: str
    platform_slug: str
    code: Optional[int]


class Platfrom(BaseModel):
    platform: PlatformDTO


class AgeRatingDTO(BaseModel):
    id: UUID4
    name: str
    type: Optional[str]
    code: Optional[int]


class AgeRating(BaseModel):
    age: AgeRatingDTO


class GamesResponseModel(GamesModel):
    age_ratings: list["AgeRating"]
    genres: list["Genre"]
    platfroms: list["Platfrom"]


class ChangeGameStatus(BaseModel):
    user_id: Optional[UUID4 | str]
    game_id: Optional[UUID4 | str]
    activity_id: Optional[UUID4 | str]


class ChangeGameFavorite(BaseModel):
    user_id: Optional[UUID4 | str]
    game_id: Optional[UUID4 | str]


class RateGame(BaseModel):
    user_id: Optional[UUID4 | str]
    game_id: UUID4
    grade: int
