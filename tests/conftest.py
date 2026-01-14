import asyncio
from typing import (
    AsyncGenerator,
    Generator,
)

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import (
    create_database,
    database_exists,
)

from auth_service.core.config import settings
from auth_service.core.database import (
    ModelBaseDeclarative,
    get_database_session,
)
from auth_service.main import create_application

pytest_plugins = [
    'tests.fixtures.dependencies',
    'tests.fixtures.users',
]


@pytest.fixture
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def test_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(
        settings.async_database_url,
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await test_engine.connect()
    transaction = await connection.begin()

    async_session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode='create_savepoint',
    )
    yield async_session

    await async_session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture(scope='session', autouse=True)
async def create_test_db() -> AsyncGenerator[None]:
    sync_engine = create_engine(settings.database_url)
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)

    ModelBaseDeclarative.metadata.create_all(bind=sync_engine)

    yield

    ModelBaseDeclarative.metadata.drop_all(bind=sync_engine)


@pytest.fixture
def app(session: AsyncSession) -> FastAPI:
    _app = create_application()

    _app.dependency_overrides[get_database_session] = lambda: session
    return _app


@pytest.fixture
async def client(app) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://test') as c:
        yield c
