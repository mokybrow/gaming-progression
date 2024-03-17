from datetime import datetime

from sqlalchemy import extract, or_

from gaming_progression_api.models.schemas import AgeRatings, Games, Genres, Platforms
from gaming_progression_api.models.service import FilterAdd


async def validate_filters(filters: FilterAdd):
    true_filters = []
    if filters.genre is not None and filters.genre != 'string' and filters.genre:
        genre = or_(Genres.name == i for i in filters.genre)
        true_filters.append(genre)
    if filters.platform is not None and filters.platform != 'string' and filters.platform:
        platform = or_(Platforms.platform_slug == i for i in filters.platform)
        true_filters.append(platform)
    if filters.age is not None and filters.age != 'string' and filters.age:
        age_rate = AgeRatings.name == filters.age
        true_filters.append(age_rate)
    if filters.release is not None and filters.release:
        release = or_(extract('year', Games.release_date) == i for i in filters.release)
        true_filters.append(release)

    return true_filters
