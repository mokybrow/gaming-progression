from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from gaming_progression_api.models.posts import GetWallModel, PostsResponseModel
from gaming_progression_api.models.walls import AddWallType, WallResponseModel
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

    async def get_user_wall_posts(self, uow: IUnitOfWork, params: GetWallModel):
        async with uow:
            user = await uow.users.find_one(username=params.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            wall_id = await uow.walls.find_one(item_id=user.id)
            if not wall_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )
            posts = await uow.posts.get_user_wall(wall_id=wall_id.id, user_id=params.user_id, page=params.page)
            print(posts)
            if not posts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )
            wall = [WallResponseModel.model_validate(row, from_attributes=True) for row in posts]

            posts_count = await uow.posts.get_posts_count(wall_id=wall_id.id)

            headers = {
                "x-post-count": f'{posts_count[0][0]}',
            }
            return JSONResponse(content=jsonable_encoder(wall), headers=headers)
