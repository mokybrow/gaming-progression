import datetime
import uuid

from uuid import UUID

from sqlalchemy import ForeignKey, Index, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gaming_progression_api.integrations.database import Base
from gaming_progression_api.models.comments import CommentsSchema
from gaming_progression_api.models.games import ChangeGameFavorite, ChangeGameStatus, GamesModel, RateGame
from gaming_progression_api.models.posts import PostsSchema
from gaming_progression_api.models.users import UserSchema
from gaming_progression_api.models.walls import WallsSchema


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=True)
    biography: Mapped[str] = mapped_column(nullable=True)
    birthdate: Mapped[datetime.date] = mapped_column(nullable=True)
    disabled: Mapped[bool] = mapped_column(default=False)

    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_moderator: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    user_activity: Mapped[list["UserActivity"]] = relationship("UserActivity")
    user_favorite: Mapped[list["UserFavorite"]] = relationship("UserFavorite")

    followers: Mapped[list["Friends"]] = relationship(
        "Friends",
        primaryjoin="Users.id==Friends.user_id",
        back_populates="follower_data",
        viewonly=True,
    )

    subscriptions: Mapped[list["Friends"]] = relationship(
        "Friends",
        primaryjoin="Users.id==Friends.follower_id",
        back_populates="sub_data",
        viewonly=True,
    )

    lists: Mapped[list["UserLists"]] = relationship(
        "UserLists",
        primaryjoin="or_(Users.id==UserLists.owner_id, Users.id==UserLists.user_id)",
        viewonly=True,
    )

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            biography=self.biography,
            birthdate=self.birthdate,
            disabled=self.disabled,
            is_verified=self.is_verified,
            is_superuser=self.is_superuser,
            is_moderator=self.is_moderator,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Games(Base):
    __tablename__ = 'games'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    cover: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    release_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    playtime: Mapped[int] = mapped_column(nullable=True)
    completed_count: Mapped[int] = mapped_column(nullable=True)
    wishlist_count: Mapped[int] = mapped_column(nullable=True)
    favorite_count: Mapped[int] = mapped_column(nullable=True)
    avg_rate: Mapped[float] = mapped_column(nullable=True)
    title_tsv = mapped_column(TSVECTOR, nullable=True, unique=False)
    __table_args__ = (Index('title_tsv_idx', 'title_tsv', postgresql_using='gin'),)

    genres: Mapped[list["GameGenres"]] = relationship(back_populates="games")
    platforms: Mapped[list["GamePlatforms"]] = relationship(back_populates="games")
    age_ratings: Mapped[list["AgeRatingsGames"]] = relationship(back_populates="games")

    def to_read_model(self) -> GamesModel:
        return GamesModel(
            id=self.id,
            title=self.title,
            cover=self.cover,
            description=self.description,
            slug=self.slug,
            release_date=self.release_date,
            playtime=self.playtime,
            completed_count=self.completed_count,
            wishlist_count=self.wishlist_count,
            favorite_count=self.favorite_count,
            avg_rate=self.avg_rate,
        )


class AgeRatings(Base):
    __tablename__ = 'age_ratings'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    code: Mapped[int] = mapped_column(nullable=True)
    age_replied: Mapped[list["AgeRatingsGames"]] = relationship(
        back_populates="age_rating",
    )


class AgeRatingsGames(Base):
    __tablename__ = 'age_rating_games'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    age_rating_id: Mapped[UUID] = mapped_column(ForeignKey("age_ratings.id"))
    __table_args__ = (UniqueConstraint('game_id', 'age_rating_id', name='_age_rating_game_uc'),)

    games: Mapped["Games"] = relationship(
        back_populates="age_ratings",
    )

    age_rating: Mapped[list["AgeRatings"]] = relationship(
        back_populates="age_replied",
    )


class Genres(Base):
    __tablename__ = 'genres'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    name_ru: Mapped[str] = mapped_column(nullable=True)
    code: Mapped[int] = mapped_column(nullable=True)

    genre_replied: Mapped[list["GameGenres"]] = relationship(
        back_populates="genre",
    )


class GameGenres(Base):
    __tablename__ = 'game_genres'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"))
    genre_id: Mapped[UUID] = mapped_column(ForeignKey("genres.id"))
    __table_args__ = (UniqueConstraint('game_id', 'genre_id', name='_game_genre_uc'),)

    games: Mapped["Games"] = relationship(
        back_populates="genres",
    )

    genre: Mapped[list["Genres"]] = relationship(
        back_populates="genre_replied",
    )


class Platforms(Base):
    __tablename__ = 'platforms'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    platform_name: Mapped[str]
    platform_name_ru: Mapped[str] = mapped_column(nullable=True)
    platform_slug: Mapped[str]
    code: Mapped[int] = mapped_column(nullable=True)

    platfrom_replied: Mapped[list["GamePlatforms"]] = relationship(
        back_populates="platform",
    )


class GamePlatforms(Base):
    __tablename__ = 'game_platforms'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    platform_id: Mapped[UUID] = mapped_column(ForeignKey("platforms.id"))

    __table_args__ = (UniqueConstraint('game_id', 'platform_id', name='_game_platform_uc'),)

    games: Mapped["Games"] = relationship(
        back_populates="platforms",
    )

    platform: Mapped[list["Platforms"]] = relationship(
        back_populates="platfrom_replied",
    )


class UserLists(Base):
    __tablename__ = 'user_lists'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    about: Mapped[str]
    is_private: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class ListGames(Base):
    __tablename__ = 'list_games'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    list_id: Mapped[UUID] = mapped_column(ForeignKey("user_lists.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    __table_args__ = (UniqueConstraint('game_id', 'list_id', name='_game_list_uc'),)


class GameReviews(Base):
    __tablename__ = 'game_reviews'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='SET NULL'))
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id", ondelete='CASCADE'))
    grade: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    __table_args__ = (UniqueConstraint('user_id', 'game_id', name='_game_review_uc'),)

    def to_read_model(self) -> RateGame:
        return RateGame(
            user_id=self.user_id,
            game_id=self.game_id,
            grade=self.grade,
        )


class Friends(Base):
    __tablename__ = 'friends'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    follower_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    follower_data: Mapped["Users"] = relationship(
        "Users",
        foreign_keys=[follower_id],
        primaryjoin="Friends.follower_id==Users.id",
    )
    sub_data: Mapped["Users"] = relationship("Users", foreign_keys=[user_id], primaryjoin="Friends.user_id==Users.id")

    __table_args__ = (UniqueConstraint('follower_id', 'user_id', name='_followers_uc'),)


class UserFavorite(Base):
    __tablename__ = 'user_favorite'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    __table_args__ = (UniqueConstraint('user_id', 'game_id', name='_user_favorite_uc'),)

    def to_read_model(self) -> ChangeGameFavorite:
        return ChangeGameFavorite(
            user_id=self.user_id,
            game_id=self.game_id,
        )


class ActivityTypes(Base):
    __tablename__ = 'activity_types'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    code: Mapped[int]


class UserActivity(Base):
    __tablename__ = 'user_activity'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    activity_id: Mapped[UUID] = mapped_column(ForeignKey("activity_types.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    activity: Mapped["ActivityTypes"] = relationship("ActivityTypes")

    __table_args__ = (UniqueConstraint('user_id', 'game_id', 'activity_id', name='_user_activity_uc'),)

    def to_read_model(self) -> ChangeGameStatus:
        return ChangeGameStatus(
            user_id=self.user_id,
            game_id=self.game_id,
            activity_id=self.activity_id,
        )


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    item_id: Mapped[UUID] = mapped_column(nullable=True)
    parent_comment_id: Mapped[UUID] = mapped_column(ForeignKey("comments.id", ondelete="RESTRICT"), nullable=True)
    text: Mapped[str]
    like_count: Mapped[int] = mapped_column(default=0)
    deleted: Mapped[bool]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    child_comment: Mapped["Comments"] = relationship("Comments")

    def to_read_model(self) -> CommentsSchema:
        return CommentsSchema(
            id=self.id,
            user_id=self.user_id,
            item_id=self.item_id,
            parent_comment_id=self.parent_comment_id,
            text=self.text,
            like_count=self.like_count,
            deleted=self.deleted,
            created_at=self.created_at,
        )


class WallTypes(Base):
    __tablename__ = 'wall_types'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    code: Mapped[int]


class Walls(Base):
    __tablename__ = 'walls'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type_id: Mapped[UUID] = mapped_column(ForeignKey("wall_types.id"))
    item_id: Mapped[UUID]
    disabled: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> WallsSchema:
        return WallsSchema(id=self.id, type_id=self.type_id, item_id=self.item_id, disabled=self.disabled)


class Posts(Base):
    __tablename__ = 'posts'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    wall_id: Mapped[UUID] = mapped_column(ForeignKey("walls.id"))
    parent_post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id", ondelete='CASCADE'))
    text: Mapped[str]
    like_count: Mapped[int] = mapped_column(default=0)
    disabled: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    def to_read_model(self) -> PostsSchema:
        return PostsSchema(
            id=self.id,
            user_id=self.user_id,
            wall_id=self.wall_id,
            parent_post_id=self.parent_post_id,
            text=self.text,
            like_count=self.like_count,
            disabled=self.disabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Tags(Base):
    __tablename__ = 'tags'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    code: Mapped[int]


class ContentTags(Base):
    __tablename__ = 'content_tags'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    item_id: Mapped[UUID]
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"))


class LikeTypes(Base):
    __tablename__ = 'like_types'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    code: Mapped[int]


class LikeLog(Base):
    __tablename__ = 'like_log'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    type_id: Mapped[UUID] = mapped_column(ForeignKey("like_types.id"))
    item_id: Mapped[UUID]
    value: Mapped[bool]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
    __table_args__ = (UniqueConstraint('user_id', 'item_id', name='_user_likes_uc'),)


class Pictures(Base):
    __tablename__ = 'pictures'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    item_id: Mapped[UUID]
    picture_path: Mapped[str]
    og_picture_path: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
