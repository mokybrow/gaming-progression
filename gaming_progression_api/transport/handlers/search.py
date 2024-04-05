from fastapi import APIRouter

from gaming_progression_api.dependencies import UOWDep
from gaming_progression_api.models.search import SearchModel
from gaming_progression_api.services.search import SearchService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/search',
    tags=['search'],
)


@router.post('/games')
async def get_game_data(uow: UOWDep, search_str: SearchModel):
    # type_adapter = TypeAdapter(GamesModel)

    result = await SearchService().search_game_tsv(uow, search_str)

    return result
