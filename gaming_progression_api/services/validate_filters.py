from datetime import datetime

from gaming_progression_api.models.schemas import AgeRatings, Games, Genres, Platforms
from gaming_progression_api.models.service import FilterAdd


async def validate_filters(filters: FilterAdd):
    true_filters = []
    if filters.genre is not None and filters.genre != 'string':
        genre = Genres.name == filters.genre
        true_filters.append(genre)
    if filters.platform is not None and filters.platform != 'string':
        platform = Platforms.platform_slug == filters.platform
        true_filters.append(platform)
    if filters.age is not None and filters.age != 'string':
        age_rate = AgeRatings.name == filters.age
        true_filters.append(age_rate)
    if filters.release is not None and filters.release > 999:
        release_start = Games.release_date <= datetime.strptime(f'{filters.release + 1}-01-01', '%Y-%m-%d').date()
        release_end = Games.release_date >= datetime.strptime(f'{filters.release}-01-01', '%Y-%m-%d').date()
        true_filters.append(release_start)
        true_filters.append(release_end)

    return true_filters
