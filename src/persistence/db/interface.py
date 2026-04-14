from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession


def get_async_engine() -> AsyncEngine:
    raise NotImplementedError


def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    raise NotImplementedError


def get_async_session() -> AsyncIterable[AsyncSession]:
    raise NotImplementedError
