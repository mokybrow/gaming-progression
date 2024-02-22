from pydantic import UUID4

from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class PostsService:
    async def create_post(self, uow: IUnitOfWork, item_id: UUID4):
        async with uow:
            post = await uow.posts.add_one(item_id=item_id)
            return post
