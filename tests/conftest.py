import asyncio

from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from gaming_progression_api.bootstrap import make_app
from gaming_progression_api.integrations.database import Base
from gaming_progression_api.settings import Settings, get_settings

main_settings = get_settings()


engine_test = create_async_engine(main_settings.database_url)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> AsyncGenerator[AsyncConnection, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield conn
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, asyncio.AbstractEventLoopPolicy, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture
def settings() -> Settings:
    return get_settings()


@fixture(name='app')
def _app() -> FastAPI:
    return make_app()


@pytest_asyncio.fixture
async def client(
    app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
