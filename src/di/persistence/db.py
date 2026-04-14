from dishka import Provider, Scope, provide

from src.persistence.db.interface import (
    get_async_engine,
    get_async_session_maker,
    get_async_session,
)
from src.persistence.db.connection import (
    async_engine_impl,
    async_session_maker_impl,
    async_session_impl,
)


class DBProvider(Provider):
    async_session_maker = provide(
        source=staticmethod(async_session_maker_impl),
        provides=get_async_session_maker,
        scope=Scope.APP,
    )

    async_session = provide(
        source=staticmethod(async_session_impl),
        provides=get_async_session,
        scope=Scope.REQUEST,
    )

    async_engine = provide(
        source=staticmethod(async_engine_impl),
        provides=get_async_engine,
        scope=Scope.APP,
    )
