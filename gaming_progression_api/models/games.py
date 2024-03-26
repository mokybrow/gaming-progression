import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class GamesModel(BaseModel):
    id: UUID4
    title: str
    cover: str | None
    description: str | None
    slug: str
    release_date: datetime.datetime | None
    playtime: int | None
    completed_count: int | None
    wishlist_count: int | None
    favorite_count: int | None
    avg_rate: float | None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GenreDTO(BaseModel):
    id: UUID4
    name: str
    name_ru: str | None
    code: int | None


class Genre(BaseModel):
    genre: GenreDTO


class PlatformDTO(BaseModel):
    id: UUID4
    platform_name: str
    platform_slug: str
    code: int | None


class Platfrom(BaseModel):
    platform: PlatformDTO


class AgeRatingDTO(BaseModel):
    id: UUID4
    name: str
    type: str | None
    code: int | None


class AgeRating(BaseModel):
    age_rating: AgeRatingDTO


class GamesResponseModel(GamesModel):
    age_ratings: list["AgeRating"]
    genres: list["Genre"]
    platforms: list["Platfrom"]

class GamesCountResponseModel(BaseModel):
    game_count: int


class ChangeGameStatus(BaseModel):
    game_id: UUID4
    activity_type: str


class ChangeGameFavorite(BaseModel):
    game_id: UUID4 | str | None


class RateGame(BaseModel):
    game_id: UUID4
    grade: int


class UserActivitySchema(BaseModel):
    id: UUID4
    user_id: UUID4
    game_id: UUID4
    activity_id: UUID4
    created_at: datetime.datetime
