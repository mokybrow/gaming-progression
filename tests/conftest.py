import asyncio

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio

from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from gaming_progression_api.bootstrap import make_app
from gaming_progression_api.integrations.database import Base, get_async_session
from gaming_progression_api.settings import Settings, get_settings

settings = get_settings()


engine_test = create_async_engine(settings.database_url_test)
async_session_maker_testing = async_sessionmaker(engine_test, expire_on_commit=False)

Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_testing() as session:
        yield session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
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
    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
