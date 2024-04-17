from fastapi import HTTPException, status
from pydantic import UUID4

from gaming_progression_api.models.likes import AddLike, AddLikeType
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class LikesService:
    async def create_new_like_type(self, uow: IUnitOfWork, like_type_data: AddLikeType):
        like_type_data_to_write = like_type_data.model_dump()
        async with uow:
            get_like_type = await uow.like_types.find_one(name=like_type_data.name)
            if get_like_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Like type with this name already exist",
                )
            add_wall_type = await uow.like_types.add_one(like_type_data_to_write)
            await uow.commit()

        return add_wall_type

    async def add_like_to_content(self, uow: IUnitOfWork, like_data: AddLike, user_id: UUID4):
        like_data_to_write = like_data.model_dump()
        async with uow:
            get_content_type = await uow.like_types.find_one(id=like_data.type_id)
            # Получаем объект для работы и его данные
            uoww = getattr(uow, get_content_type.name)
            item_data = await uoww.find_one(id=like_data.item_id)
            get_like = await uow.likes.find_one(user_id=user_id, item_id=like_data.item_id)
            # Удаляем лайк и уменьшаем счётчик у объекта
            if get_like and get_like.value is True:
                like_id = await uow.likes.edit_one(data={"value": False}, user_id=user_id, item_id=like_data.item_id)
                await uoww.edit_one(data={"likes_count": item_data.likes_count - 1}, id=like_data.item_id)
                await uow.commit()
                return f"like with ID {like_id} from {user_id} was successfully deleted"
            # Добавляем лайк и увеличивем счётчик у объекта
            if get_like and get_like.value is False:
                like_id = await uow.likes.edit_one(data={"value": True}, user_id=user_id, item_id=like_data.item_id)
                await uoww.edit_one(data={"likes_count": item_data.likes_count + 1}, id=like_data.item_id)

                await uow.commit()
                return f"like with ID {like_id} from {user_id} was successfully added"
            # Записываем лайк и увеличивем счётчик у объекта
            like_data_to_write["user_id"] = user_id
            like_id = await uow.likes.add_one(like_data_to_write)
            await uoww.edit_one(data={"likes_count": item_data.likes_count + 1}, id=like_data.item_id)

            await uow.commit()
            return f"like with ID {like_id} from {user_id} was successfully added"
