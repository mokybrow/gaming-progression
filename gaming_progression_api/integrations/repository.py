from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gaming_progression_api.models.schemas import AgeRatingsGames, Friends, GameGenres, GamePlatforms, UserActivity


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = Any

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict) -> UUID4:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_all(self) -> list | bool:
        query = select(self.model)
        result = await self.session.execute(query)
        result = [row[0].to_read_model() for row in result.all()]
        return result

    async def find_one(self, **filter_by) -> dict | bool:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            result = result.scalar_one().to_read_model()
            return result
        except:
            return False

    async def edit_one(self, data: dict, **filter_by) -> UUID4:
        stmt = update(self.model).values(data).filter_by(**filter_by).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, **filter_by) -> dict | bool:
        query = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            result = result.scalars().all()
            return result
        except:
            return False

    # ------------------------------>
    async def find_one_comment(self, **filter_by) -> dict | bool:
        query = select(self.model).options(selectinload(self.model.child_comment)).filter_by(**filter_by)
        result = await self.session.execute(query)
        self.session.expunge_all()
        try:
            result = result.scalars().all()
            return result
        except:
            return False

    async def find_one_user(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.user_activity).selectinload(UserActivity.activity))
            .options(selectinload(self.model.user_favorite))
            .options(selectinload(self.model.followers).selectinload(Friends.follower_data))
            .options(selectinload(self.model.subscriptions).selectinload(Friends.sub_data))
            .options(selectinload(self.model.lists))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().one()
            return result
        except:
            return False

    async def find_one_game(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.platfroms).selectinload(GamePlatforms.platform))
            .options(selectinload(self.model.genres).selectinload(GameGenres.genre))
            .options(selectinload(self.model.age_ratings).selectinload(AgeRatingsGames.age))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().all()
            return result
        except:
            return False

    async def find_all_games_with_filters(self, limit: int | None, filters: list, sort: str | None = None):
        query = (
            select(self.model)
            .join(self.model.genres)
            .join(GameGenres.genre)
            .join(self.model.platforms)
            .join(GamePlatforms.platform)
            .join(self.model.age_ratings)
            .join(AgeRatingsGames.age_rating)
            .options(selectinload(self.model.genres).selectinload(GameGenres.genre))
            .options(selectinload(self.model.platforms).selectinload(GamePlatforms.platform))
            .options(selectinload(self.model.age_ratings).selectinload(AgeRatingsGames.age_rating))
            .filter(*filters)
            .limit(limit)
            .order_by(sort)
            .distinct()
        )
        result = await self.session.execute(query)
        self.session.expunge_all()
        try:
            result = result.scalars().all()
            return result
        except:
            return False
