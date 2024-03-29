from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4
from sqlalchemy import and_, case, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager

from gaming_progression_api.models.schemas import (
    AgeRatings,
    AgeRatingsGames,
    Friends,
    GameGenres,
    GamePlatforms,
    Genres,
    LikeLog,
    ListGames,
    Platforms,
    UserActivity,
    UserFavorite,
    UserLists,
)


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

    async def add_many(self, data: list) -> UUID4:
        stmt = insert(self.model).values(data)
        result = await self.session.execute(stmt)
        # return result.scalar_one()

    async def find_all(self, limit: int | None = None, offset: int | None = None) -> list | bool:
        query = select(self.model).limit(limit).offset(offset)
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
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_one(self, **filter_by) -> dict | bool:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        result = await self.session.execute(stmt)
        try:
            result = result.scalar_one()
            return result
        except:
            return False

    async def search_by_field(self, *filter_by) -> dict | bool:
        query = select(self.model).filter(*filter_by)
        result = await self.session.execute(query)
        result = [row[0].to_read_model() for row in result.all()]
        return result
    # ------------------------------>
    async def find_one_comment(self, **filter_by) -> dict | bool:
        query = (
            select(self.model, 
                   )
            .options(selectinload(self.model.child_comment).selectinload(self.model.author_info))
            .options(selectinload(self.model.author_info))
            .filter_by(**filter_by)
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().all()
            return result
        except:
            return False
        

    async def check_user_comments_like(self, item_id: UUID4, user_id: UUID4) -> dict | bool:
        query = (
            select(self.model.id, 
                   func.sum(case((and_(LikeLog.user_id == user_id, LikeLog.item_id == self.model.id, LikeLog.value==True), 1), else_=0))
                   .label('hasAuthorLike')
                   )

            .filter_by(item_id=item_id)
            .group_by(self.model.id)
        )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.all()
            return result
        except:
            return False
        

    async def find_one_user(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.user_activity).selectinload(UserActivity.game_data))
            .options(selectinload(self.model.user_activity).selectinload(UserActivity.activity_data))
            .options(selectinload(self.model.user_favorite).selectinload(UserFavorite.game_data))
            .options(selectinload(self.model.followers).selectinload(Friends.follower_data))
            .options(selectinload(self.model.subscriptions).selectinload(Friends.sub_data))
            .options(selectinload(self.model.lists).selectinload(UserLists.playlists))
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
            .options(selectinload(self.model.platforms).selectinload(GamePlatforms.platform))
            .options(selectinload(self.model.genres).selectinload(GameGenres.genre))
            .options(selectinload(self.model.age_ratings).selectinload(AgeRatingsGames.age_rating))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().all()
            return result
        except:
            return False

    async def find_all_games_with_filters(
        self,
        limit: int | None,
        offset: int | None,
        filters: list,
        sort: str | None = None,
    ):
        query = (
            select(self.model)
            .join(GameGenres, isouter=True)
            .join(Genres, isouter=True)
            .join(GamePlatforms, isouter=True)
            .join(Platforms, isouter=True)
            .join(AgeRatingsGames, isouter=True)
            .join(AgeRatings, isouter=True)
            .options(selectinload(self.model.genres).selectinload(GameGenres.genre))
            .options(selectinload(self.model.platforms).selectinload(GamePlatforms.platform))
            .options(selectinload(self.model.age_ratings).selectinload(AgeRatingsGames.age_rating))
            .filter(*filters)
            .limit(limit)
            .offset(offset)
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

    async def get_games_count_with_filters(
        self,
        filters: list,
    ):
        query = (
            select(func.count(self.model.id.distinct()).label("game_count"))
            .join(GameGenres, isouter=True)
            .join(Genres, isouter=True)
            .join(GamePlatforms, isouter=True)
            .join(Platforms, isouter=True)
            .join(AgeRatingsGames, isouter=True)
            .join(AgeRatings, isouter=True)
            .filter(*filters)
        )
        result = await self.session.execute(query)
        try:
            result = result.all()
            return result
        except:
            return False
        
    async def get_playlist_data(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.list_games).selectinload(ListGames.game_data))
            .options(selectinload(self.model.owner_data))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().all()
            return result
        except:
            return False

    async def get_mailing_settings(self, **filter_by):
        query = select(self.model).options(selectinload(self.model.type_data)).filter_by(**filter_by)
        result = await self.session.execute(query)
        self.session.expunge_all()

        try:
            result = result.scalars().all()
            return result
        except:
            return False
