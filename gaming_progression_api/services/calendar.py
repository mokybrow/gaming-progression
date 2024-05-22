from datetime import timedelta

from fastapi import HTTPException, status

from gaming_progression_api.models.games import GamesResponseModel
from gaming_progression_api.models.schemas import Games
from gaming_progression_api.models.service import GetFamesByMonth
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

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
            games = [GamesResponseModel.model_validate(row, from_attributes=True) for row in games]
            grouped_games = {}
            games_list = []
            for i in games:
                if i.release_date.day in grouped_games:
                    grouped_games[i.release_date.day] = grouped_games[i.release_date.day] + [i]
                else:
                    games_list.append(grouped_games.copy())
                    grouped_games.clear()
                    grouped_games[i.release_date.day] = [i]
            return games_list