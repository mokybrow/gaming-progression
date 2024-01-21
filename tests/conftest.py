from collections.abc import AsyncGenerator

import pytest_asyncio

from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from service_api.bootstrap import make_app
from service_api.settings import Settings, get_settings


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
