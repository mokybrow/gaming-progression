from fastapi import HTTPException, status

from gaming_progression_api.models.walls import AddWallType
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class WallsService:
    async def create_new_wall_type(self, uow: IUnitOfWork, wall_type_data: AddWallType):
        async with uow:
            get_wall_type = await uow.wall_types.find_one(name=wall_type_data.name)
            if get_wall_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Wall type with this name already exist",
                )
            wall_type_data = wall_type_data.model_dump()
            add_wall_type = await uow.wall_types.add_one(wall_type_data)
            await uow.commit()

        return add_wall_type
