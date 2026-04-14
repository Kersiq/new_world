from typing import AsyncIterable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from src.core.config import config
from src.persistence.db.interface import get_async_engine, get_async_session_maker


async def async_engine_impl() -> AsyncEngine:
    return create_async_engine(
        config.db.get_postgres_dsn(),
        pool_pre_ping=True,
        pool_size=config.db.pool_max_size,
        max_overflow=10,
        pool_recycle=7200,
    )



async def async_session_maker_impl(
    engine: get_async_engine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )


async def async_session_impl(
    session_maker: get_async_session_maker,
) -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
