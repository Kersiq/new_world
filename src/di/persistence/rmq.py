from dishka import Provider, Scope, provide


from src.persistence.rmq.faststream.interface import (
    get_rabbit_broker,
    get_rmq_service,
)
from src.persistence.rmq.faststream.connection import (
    rabbit_broker_impl,
    rmq_service_impl,
)


class RMQProvider(Provider):

    broker = provide(
        source=staticmethod(rabbit_broker_impl),
        provides=get_rabbit_broker,
        scope=Scope.REQUEST,
    )

    rmq_service = provide(
        source=staticmethod(rmq_service_impl),
        provides=get_rmq_service,
        scope=Scope.REQUEST,
    )