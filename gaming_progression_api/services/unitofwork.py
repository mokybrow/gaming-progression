from abc import ABC, abstractmethod

from gaming_progression_api.integrations.comments import CommentsRepository
from gaming_progression_api.integrations.database import async_session_maker
from gaming_progression_api.integrations.followers import FollowersRepository
from gaming_progression_api.integrations.game_statuses import ActivityTypesRepository, FavoriteRepository, StatusesRepository
from gaming_progression_api.integrations.games import GamesRepository, GamesReviewsRepository
from gaming_progression_api.integrations.likes import LikesRepository, LikeTypesRepository
from gaming_progression_api.integrations.playlists import AddPlaylistsRepository, CreatePlaylistsRepository
from gaming_progression_api.integrations.posts import PostsRepository
from gaming_progression_api.integrations.users import UsersRepository
from gaming_progression_api.integrations.walls import WallsRepository, WallsTypesRepository


class IUnitOfWork(ABC):
    users: type[UsersRepository]
    games: type[GamesRepository]
    statuses: type[StatusesRepository]
    favorite: type[FavoriteRepository]
    rates: type[GamesReviewsRepository]
    comments: type[CommentsRepository]
    posts: type[PostsRepository]
    walls: type[WallsRepository]
    wall_types: type[WallsTypesRepository]
    likes: type[LikesRepository]
    like_types: type[LikeTypesRepository]
    playlists: type[CreatePlaylistsRepository]
    add_playlists: type[AddPlaylistsRepository]
    followers: type[FollowersRepository]
    activity_types: type[ActivityTypesRepository]

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    async def __aenter__(self) -> None:
        ...

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.games = GamesRepository(self.session)
        self.statuses = StatusesRepository(self.session)
        self.favorite = FavoriteRepository(self.session)
        self.rates = GamesReviewsRepository(self.session)
        self.comments = CommentsRepository(self.session)
        self.posts = PostsRepository(self.session)
        self.walls = WallsRepository(self.session)
        self.wall_types = WallsTypesRepository(self.session)
        self.likes = LikesRepository(self.session)
        self.like_types = LikeTypesRepository(self.session)
        self.playlists = CreatePlaylistsRepository(self.session)
        self.add_playlists = AddPlaylistsRepository(self.session)
        self.followers = FollowersRepository(self.session)
        self.activity_types = ActivityTypesRepository(self.session)

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
