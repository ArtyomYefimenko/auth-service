import logging
from typing import (
    Annotated,
    AsyncGenerator,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from auth_service.core.config import settings

logger = logging.getLogger(__name__)


async_engine = create_async_engine(
    settings.async_database_url,
    echo=settings.database_log_queries,
    pool_pre_ping=True,
    future=True,
    pool_size=settings.database_pool_max_size,
    max_overflow=0,
    pool_timeout=settings.database_pool_timeout,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception('DB transaction failed')
            raise


ModelBaseDeclarative = declarative_base()

DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]
