from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gaming_progression_api.models.schemas import GameGenres, Games


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


    async def find_one_relation(self, **filter_by) :
        query = (select(self.model)
                 .options(selectinload(Games.genre))
                 .filter_by(**filter_by)
                 )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().all()
            return result
        except:
            return False