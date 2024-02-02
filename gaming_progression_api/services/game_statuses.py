from datetime import datetime

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import asc, desc

from gaming_progression_api.models.games import ChangeGameStatus, GamesResponseModel
from gaming_progression_api.models.schemas import AgeRatings, Games, Genres, Platforms
from gaming_progression_api.models.service import FilterAdd
from gaming_progression_api.models.users import PatchUser, UserCreate
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class StatusesService:
    async def change_status(self, uow: IUnitOfWork, new_status: ChangeGameStatus, user_id: UUID4):
        async with uow:
            unique_string = await uow.status.find_one(
                user_id=user_id, game_id=new_status.game_id, activity_id=new_status.activity_id
            )
            if unique_string:
                await uow.status.delete_one(user_id=user_id)
                await uow.commit()
                return False

            change_data = await uow.status.find_one(user_id=user_id, game_id=new_status.game_id)
            if change_data:
                await uow.status.edit_one(data={'activity_id': new_status.activity_id})
                await uow.commit()
                return True
            new_status = new_status.model_dump()
            new_status['user_id'] = user_id
            status = await uow.status.add_one(new_status)
            await uow.commit()
            return status
