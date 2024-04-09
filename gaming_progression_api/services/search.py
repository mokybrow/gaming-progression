from gaming_progression_api.models.search import SearchModel
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.services.validate_filters import validate_filters_for_search
from gaming_progression_api.settings import get_settings

settings = get_settings()


class SearchService:
    async def search_game_tsv(self, uow: IUnitOfWork, search_words: SearchModel):
        true_filters = await validate_filters_for_search(search_words)
        if not true_filters:
            return False
        async with uow:
            presence_of_wall = await uow.games.search_game(true_filters, search_words.limit)
            return presence_of_wall

    async def search_game_count(self, uow: IUnitOfWork, search_words: SearchModel):
        true_filters = await validate_filters_for_search(search_words)
        if not true_filters:
            return False
        async with uow:
            presence_of_wall = await uow.games.search_game_count(true_filters)
            print(presence_of_wall[0])
            return presence_of_wall[0]