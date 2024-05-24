import json

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy import or_

from gaming_progression_api.models.feeds import FeedResponseModel
from gaming_progression_api.models.games import ChangeGameFavorite, ChangeGameStatus
from gaming_progression_api.models.posts import PostsResponseModel
from gaming_progression_api.models.schemas import Posts
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class FeedsService:
    async def get_global_feed_for_auth(self, uow: IUnitOfWork, page: int, user_id: UUID4):
        async with uow:
            user_subs = await uow.followers.find_all_with_filters(follower_id=user_id)
            if not user_subs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no subs",
                )
            true_filters = []
            filters = or_(Posts.user_id == i.user_id for i in user_subs)
            true_filters.append(filters)
            true_filters.append(Posts.disabled==False)
            posts = await uow.posts.get_global_wall_for_auth(filters=true_filters, page=page, user_id=user_id)
            posts = [FeedResponseModel.model_validate(row, from_attributes=True) for row in posts]
            if not posts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User have no posts",
                )

            posts_count = await uow.posts.get_posts_count_for_wall(filters=true_filters)
            headers = {
                "x-post-count": f'{posts_count[0][0]}',
            }
            return JSONResponse(content=jsonable_encoder(posts), headers=headers)
