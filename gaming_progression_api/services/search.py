from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import exc

from gaming_progression_api.models.posts import AddPost, DeletePost
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
            presence_of_wall = await uow.games.search_game(true_filters)
            return presence_of_wall