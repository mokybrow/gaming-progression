from sqlalchemy import extract, or_

from gaming_progression_api.models.schemas import AgeRatings, Games, Genres, Platforms
from gaming_progression_api.models.search import SearchModel
from gaming_progression_api.models.service import FilterAdd


async def validate_filters(filters: FilterAdd):
    true_filters = []
    if filters.genre != None and filters.genre:
        genre = or_(Genres.code == i for i in filters.genre)
        true_filters.append(genre)
    if filters.platform != None and filters.platform:
        platform = or_(Platforms.code == i for i in filters.platform)
        true_filters.append(platform)
    if filters.age != None and filters.age:
        age_rate = or_(AgeRatings.code == i for i in filters.age)
        true_filters.append(age_rate)
    if filters.release != None and filters.release:
        release = or_(extract('year', Games.release_date) == i for i in filters.release)
        true_filters.append(release)

    return true_filters


async def validate_filters_for_search(filters: SearchModel):
    filters = filters.search_string.split()

    true_filters = []
    if filters:
        for i in filters:
            games = or_(Games.title_tsv.match(i))
            true_filters.append(games)

    return true_filters
