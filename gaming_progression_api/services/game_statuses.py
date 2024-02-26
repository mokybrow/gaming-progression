
from fastapi import HTTPException, status
from pydantic import UUID4

from gaming_progression_api.models.games import ChangeGameFavorite, ChangeGameStatus
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class StatusesService:
    async def change_status(self, uow: IUnitOfWork, new_status: ChangeGameStatus, user_id: UUID4):
        async with uow:
            activity_id = await uow.activity_types.find_one(name=new_status.activity_type)
            if not activity_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Activity type not found',
                )
            unique_string = await uow.statuses.find_one(
                user_id=user_id, game_id=new_status.game_id, activity_id=activity_id.id,
            )
            if unique_string:
                await uow.statuses.delete_one(user_id=user_id, game_id=new_status.game_id)
                await uow.commit()
                raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail=f'Game {new_status.game_id} status deleted successfully',
                )

            change_data = await uow.statuses.find_one(user_id=user_id, game_id=new_status.game_id)
            if change_data:
                await uow.statuses.edit_one(data={'activity_id': activity_id.id}, user_id=user_id, game_id=new_status.game_id)
                await uow.commit()
                raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail=f'Game {new_status.game_id} status changed to {activity_id.id}',
                )
            new_status = new_status.model_dump()
            del new_status["activity_type"]
            new_status['user_id'] = user_id
            new_status['activity_id'] = activity_id.id

            await uow.statuses.add_one(new_status)
            await uow.commit()
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'Game {new_status['game_id']} added status {new_status['activity_id']}',
            )

    async def change_favorite(self, uow: IUnitOfWork, new_favorite: ChangeGameFavorite, user_id: UUID4):
        async with uow:
            unique_string = await uow.favorite.find_one(user_id=user_id, game_id=new_favorite.game_id)
            if unique_string:
                await uow.favorite.delete_one(user_id=user_id)
                await uow.commit()
                raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f'Game with {new_favorite.game_id} deleted successfully',
        headers={'WWW-Authenticate': 'Bearer'},
    )

            add_to_favorite = new_favorite.model_dump()
            add_to_favorite['user_id'] = user_id
            add_to_favorite = await uow.favorite.add_one(add_to_favorite)
            await uow.commit()
            raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f'Game with {new_favorite.game_id} added successfully',
            headers={'WWW-Authenticate': 'Bearer'},
        )
