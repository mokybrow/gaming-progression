from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4
from sqlalchemy import and_, case, delete, desc, distinct, func, funcfilter, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gaming_progression_api.models.schemas import (
    AgeRatings,
    AgeRatingsGames,
    Comments,
    Friends,
    GameGenres,
    GamePlatforms,
    Genres,
    LikeLog,
    ListGames,
    Platforms,
    Posts,
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
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def add_many(self, data: list) -> UUID4:
        stmt = insert(self.model).values(data)
        await self.session.execute(stmt)
        # return result.scalar_one()

    async def find_all(self, limit: int | None = None, offset: int | None = None) -> list | bool:
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        result = [row[0].to_read_model() for row in result.all()]
        return result

    async def find_all_with_filters(self, **filter_by) -> list | bool:
        query = select(self.model).filter_by(**filter_by)
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
    async def get_content_comments(self, user_id: UUID4, **filter_by) -> dict | bool:
        query = (
            select(self.model)
            .options(selectinload(self.model.child_comment).selectinload(self.model.author_data))
            .options(selectinload(self.model.author_data))
            .group_by(self.model.id)
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

    async def get_comments_count(self, **filter_by) -> dict | bool:
        query = select(func.count(self.model.id.distinct()).label("comments_count")).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            result = result.all()
            return result
        except:
            return False

    async def check_user_comments_like(self, item_id: UUID4, user_id: UUID4) -> dict | bool:
        query = (
            select(
                self.model.id,
                func.sum(
                    case(
                        (and_(LikeLog.user_id == user_id, LikeLog.item_id == self.model.id, LikeLog.value == True), 1),
                        else_=0,
                    ),
                ).label('hasAuthorLike'),
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
            select(
                self.model,
            )
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
        page: int | None,
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
            .limit(20)
            .offset(page)
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

    async def search_game(self, filters: list, limit: int):
        query = select(self.model).filter(*filters).limit(limit)
        result = await self.session.execute(query)
        self.session.expunge_all()
        try:
            result = result.scalars().all()
            return result
        except:
            return False

    async def search_game_count(self, filters: list):
        query = select(func.count(self.model.id).label("game_count")).filter(*filters)

        result = await self.session.execute(query)
        self.session.expunge_all()
        try:
            result = result.all()
            return result
        except:
            return False

    async def get_user_posts(self, offset: int = 10, **filter_by) -> dict | bool:
        query = (
            select(
                self.model,
                funcfilter(func.count(distinct(Comments.id)), Comments.item_id == self.model.id).label('commentCount'),
            )
            .filter_by(**filter_by)
            .options(selectinload(self.model.parent_post_data).selectinload(self.model.users))
            .options(selectinload(self.model.users))
            .group_by(self.model.id)
            .limit(offset)
            .order_by(desc(self.model.created_at))
        )
        result = await self.session.execute(query)
        self.session.expunge_all()
        try:
            result = result.all()
            return result
        except:
            return False

    async def get_user_wall(self, user_id: UUID4, page: int = 10, **filter_by) -> dict | bool:
        query = (
            select(
                self.model,
                func.sum(
                    distinct(
                        case(
                            (
                                and_(
                                    LikeLog.user_id == user_id,
                                    LikeLog.item_id == self.model.id,
                                    LikeLog.value == True,
                                ),
                                1,
                            ),
                            else_=0,
                        ),
                    ),
                ).label('hasAuthorLike'),
            )
            .filter_by(**filter_by)
            .options(selectinload(self.model.parent_post_data).selectinload(self.model.author_data))
            .options(selectinload(self.model.author_data))
            .group_by(self.model.id)
            .order_by(desc(self.model.created_at))
            .limit(10)
            .offset(page)
        )
        result = await self.session.execute(query)
        print(query)
        self.session.expunge_all()
        try:
            result = result.all()
            return result
        except:
            return False

    async def get_post(self, user_id: UUID4, **filter_by) -> dict | bool:
        query = (
            select(
                self.model,
                func.sum(
                    distinct(
                        case(
                            (
                                and_(
                                    LikeLog.user_id == user_id,
                                    LikeLog.item_id == self.model.id,
                                    LikeLog.value == True,
                                ),
                                1,
                            ),
                            else_=0,
                        ),
                    ),
                ).label('hasAuthorLike'),
            )
            .filter_by(**filter_by)
            .options(selectinload(self.model.parent_post_data).selectinload(self.model.author_data))
            .options(selectinload(self.model.author_data))
            .group_by(self.model.id)
            .order_by(desc(self.model.created_at))
        )
        result = await self.session.execute(query)
        self.session.expunge_all()
        try:
            result = result.all()
            return result
        except:
            return False

    async def get_posts_count(self, **filter_by) -> dict | bool:
        query = select(func.count(self.model.id.distinct()).label("posts_count")).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            result = result.all()
            return result
        except:
            return False

    async def get_global_wall_for_auth(self, filters: list, user_id: UUID4, page: int = 10) -> dict | bool:
        query = (
            select(
                self.model,
                func.sum(
                    distinct(
                        case(
                            (
                                and_(
                                    LikeLog.user_id == user_id,
                                    LikeLog.item_id == self.model.id,
                                    LikeLog.value == True,
                                ),
                                1,
                            ),
                            else_=0,
                        ),
                    ),
                ).label('hasAuthorLike'),
            )
            .options(selectinload(self.model.parent_post_data).selectinload(self.model.author_data))
            .options(selectinload(self.model.author_data))
            .filter(*filters)
            .group_by(self.model.id)
            .order_by(desc(self.model.created_at))
            .limit(10)
            .offset(page)
        )
        result = await self.session.execute(query)

        self.session.expunge_all()
        try:
            result = result.all()
            return result
        except:
            return False

    async def get_posts_count_for_wall(self, filters: list) -> dict | bool:
        query = select(func.count(self.model.id.distinct()).label("posts_count")).filter(*filters)
        result = await self.session.execute(query)
        try:
            result = result.all()
            return result
        except:
            return False
