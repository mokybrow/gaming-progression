import datetime
import uuid

from uuid import UUID

from sqlalchemy import ForeignKey, Index, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gaming_progression_api.integrations.database import Base
from gaming_progression_api.models.comments import CommentsSchema
from gaming_progression_api.models.followers import FollowersSchema
from gaming_progression_api.models.games import ChangeGameFavorite, GamesModel, RateGame, UserActivitySchema
from gaming_progression_api.models.likes import LikeLogSchema
from gaming_progression_api.models.playlists import AddGameListSchema, PlaylistsSchema, UserListsSchema
from gaming_progression_api.models.posts import PostsSchema
from gaming_progression_api.models.service import ObjectTypesSchema
from gaming_progression_api.models.users import UserMailingsSchema, UserSchema
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

    user_activity: Mapped[list["UserActivity"]] = relationship(back_populates="users")
    user_favorite: Mapped[list["UserFavorite"]] = relationship(back_populates="users")

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

    lists: Mapped[list["UserLists"]] = relationship(back_populates="users")

    sub_data: Mapped["Playlists"] = relationship("Playlists", primaryjoin="Playlists.owner_id==Users.id")

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

    user_fav_replied: Mapped[list["UserFavorite"]] = relationship(
        back_populates="game_data",
    )
    user_act_replied: Mapped[list["UserActivity"]] = relationship(
        back_populates="game_data",
    )

    list_data_replied: Mapped[list["ListGames"]] = relationship(
        back_populates="game_data",
    )

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


class Playlists(Base):
    __tablename__ = 'playlists'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    about: Mapped[str] = mapped_column(nullable=True)
    is_private: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    playlists_replied: Mapped[list["UserLists"]] = relationship(
        back_populates="playlists",
    )

    list_games: Mapped[list["ListGames"]] = relationship(
        back_populates="playlists",
    )
    owner_data: Mapped[list["Users"]] = relationship(
        "Users",
        primaryjoin="Users.id==Playlists.owner_id",
        back_populates="sub_data",
        viewonly=True,
    )

    def to_read_model(self) -> PlaylistsSchema:
        return PlaylistsSchema(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            about=self.about,
            is_private=self.is_private,
            created_at=self.created_at,
        )


class UserLists(Base):
    __tablename__ = 'user_lists'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    list_id: Mapped[UUID] = mapped_column(ForeignKey("playlists.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    __table_args__ = (UniqueConstraint('user_id', 'list_id', name='_user_one_list_uc'),)

    users: Mapped["Users"] = relationship(
        back_populates="lists",
    )
    playlists: Mapped[list["Playlists"]] = relationship(
        back_populates="playlists_replied",
    )

    def to_read_model(self) -> UserListsSchema:
        return UserListsSchema(id=self.id, list_id=self.list_id, user_id=self.user_id, created_at=self.created_at)


class ListGames(Base):
    __tablename__ = 'list_games'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    list_id: Mapped[UUID] = mapped_column(ForeignKey("playlists.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    __table_args__ = (UniqueConstraint('game_id', 'list_id', name='_game_list_uc'),)

    playlists: Mapped[list["Playlists"]] = relationship(
        back_populates="list_games",
    )

    game_data: Mapped[list["Games"]] = relationship(
        back_populates="list_data_replied",
    )

    def to_read_model(self) -> AddGameListSchema:
        return AddGameListSchema(id=self.id, game_id=self.game_id, list_id=self.list_id, created_at=self.created_at)


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

    def to_read_model(self) -> FollowersSchema:
        return FollowersSchema(
            id=self.id,
            user_id=self.user_id,
            follower_id=self.follower_id,
            created_at=self.created_at,
        )


class UserFavorite(Base):
    __tablename__ = 'user_favorite'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    __table_args__ = (UniqueConstraint('user_id', 'game_id', name='_user_favorite_uc'),)

    users: Mapped["Users"] = relationship(
        back_populates="user_favorite",
    )
    game_data: Mapped[list["Games"]] = relationship(
        back_populates="user_fav_replied",
    )

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

    activity_type: Mapped[list["UserActivity"]] = relationship(
        back_populates="activity_data",
    )

    def to_read_model(self) -> ObjectTypesSchema:
        return ObjectTypesSchema(
            id=self.id,
            name=self.name,
            code=self.code,
        )


class UserActivity(Base):
    __tablename__ = 'user_activity'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id"))
    activity_id: Mapped[UUID] = mapped_column(ForeignKey("activity_types.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    users: Mapped["Users"] = relationship(
        back_populates="user_activity",
    )
    game_data: Mapped[list["Games"]] = relationship(
        back_populates="user_act_replied",
    )
    activity_data: Mapped[list["ActivityTypes"]] = relationship(
        back_populates="activity_type",
    )

    __table_args__ = (UniqueConstraint('user_id', 'game_id', 'activity_id', name='_user_activity_uc'),)

    def to_read_model(self) -> UserActivitySchema:
        return UserActivitySchema(
            id=self.id,
            user_id=self.user_id,
            game_id=self.game_id,
            activity_id=self.activity_id,
            created_at=self.created_at,
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
    author_info: Mapped["Users"] = relationship("Users", primaryjoin="Users.id==Comments.user_id")

    child_comment: Mapped[list["Comments"]] = relationship(
        "Comments", primaryjoin="Comments.id == Comments.parent_comment_id", order_by='Comments.created_at.asc()'
    )

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

    def to_read_model(self) -> ObjectTypesSchema:
        return ObjectTypesSchema(
            id=self.id,
            name=self.name,
            code=self.code,
        )


class Walls(Base):
    __tablename__ = 'walls'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type_id: Mapped[UUID] = mapped_column(ForeignKey("wall_types.id"))
    item_id: Mapped[UUID]

    def to_read_model(self) -> WallsSchema:
        return WallsSchema(id=self.id, type_id=self.type_id, item_id=self.item_id)


class Posts(Base):
    __tablename__ = 'posts'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    wall_id: Mapped[UUID] = mapped_column(ForeignKey("walls.id"))
    parent_post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id", ondelete='CASCADE'), nullable=True)
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

    def to_read_model(self) -> ObjectTypesSchema:
        return ObjectTypesSchema(
            id=self.id,
            name=self.name,
            code=self.code,
        )


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

    def to_read_model(self) -> ObjectTypesSchema:
        return ObjectTypesSchema(
            id=self.id,
            name=self.name,
            code=self.code,
        )


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

    def to_read_model(self) -> LikeLogSchema:
        return LikeLogSchema(
            id=self.id,
            user_id=self.user_id,
            type_id=self.type_id,
            item_id=self.item_id,
            value=self.value,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


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


class UserMailings(Base):
    __tablename__ = 'user_mailings'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    mailing_id: Mapped[UUID] = mapped_column(ForeignKey("mailing_types.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    __table_args__ = (UniqueConstraint('user_id', 'mailing_id', name='_user_mailing_uc'),)

    type_data: Mapped[list["MailingTypes"]] = relationship(
        back_populates="mailing_type",
    )

    def to_read_model(self) -> UserMailingsSchema:
        return UserMailingsSchema(
            id=self.id,
            user_id=self.user_id,
            mailing_id=self.mailing_id,
            created_at=self.created_at,
        )


class MailingTypes(Base):
    __tablename__ = 'mailing_types'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    code: Mapped[int]

    mailing_type: Mapped[list["UserMailings"]] = relationship(
        back_populates="type_data",
    )

    def to_read_model(self) -> ObjectTypesSchema:
        return ObjectTypesSchema(
            id=self.id,
            name=self.name,
            code=self.code,
        )
