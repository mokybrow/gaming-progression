from abc import ABC, abstractmethod

from gaming_progression_api.integrations.database import async_session_maker
from gaming_progression_api.integrations.game_statuses import FavoriteRepository, StatusesRepository
from gaming_progression_api.integrations.games import GamesRepository, GamesReviewsRepository
from gaming_progression_api.integrations.users import UsersRepository


class IUnitOfWork(ABC):
    users: type[UsersRepository]
    games: type[GamesRepository]
    statuses: type[StatusesRepository]
    favorite: type[FavoriteRepository]
    rates: type[GamesReviewsRepository]

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

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
