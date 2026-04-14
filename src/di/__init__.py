from dishka import make_async_container, AsyncContainer

from src.di.persistence.db import DBProvider


async def get_async_container() -> AsyncContainer:

        db_provider = DBProvider()

        return make_async_container(
                db_provider,
        )