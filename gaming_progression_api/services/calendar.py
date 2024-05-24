from datetime import timedelta

from fastapi import HTTPException, status

from gaming_progression_api.models.games import GamesResponseModel
from gaming_progression_api.models.schemas import Games
from gaming_progression_api.models.service import GetFamesByMonth
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings
from collections import Counter
from itertools import groupby
from operator import itemgetter

settings = get_settings()


class CalendarService:
    async def get_games_by_mont(self, uow: IUnitOfWork,     data: GetFamesByMonth,):
        next_month_date = data.date + timedelta(days=data.days  )
        async with uow:
            filters = [Games.release_date >= data.date.replace(tzinfo=None), Games.release_date < next_month_date.replace(tzinfo=None)]
            games = await uow.games.games_by_month(filters=filters)
            if not games:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Games not found",
            )
            # print(games)
            games = [GamesResponseModel.model_validate(row, from_attributes=True) for row in games]
            games_list = []
            keyfunc = lambda x:x.release_date.day
            tasks = sorted(games, key=keyfunc)
            for task, action in groupby(tasks , key=keyfunc):
                order_action = sorted(action, key=lambda x:x.release_date.day)
                games_list.append({task: order_action})

            return games_list