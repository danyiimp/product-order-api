from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import TEST_DATABASE_URL
from app.core.database import Base, get_async_session
from app.main import app
from app.models import *  # noqa: F403


@pytest.fixture(scope="session")
def async_session_maker():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_environment(async_session_maker):
    engine = async_session_maker.kw["bind"]
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def db(async_session_maker):
    engine = async_session_maker.kw["bind"]
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            session = AsyncSession(bind=connection, expire_on_commit=False)

            async def override_get_async_session() -> AsyncGenerator[
                AsyncSession, None
            ]:
                yield session

            app.dependency_overrides[get_async_session] = (
                override_get_async_session
            )

            yield session

            await transaction.rollback()

            app.dependency_overrides.clear()


@pytest.fixture(scope="module")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
