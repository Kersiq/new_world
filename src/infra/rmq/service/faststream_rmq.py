from typing import Any

from src.application.interfaces.services.i_rmq import IRMQService
from src.persistence.rmq.faststream.interface import get_rabbit_broker


class FastStreamRMQService(IRMQService):
    def __init__(self, broker: get_rabbit_broker):
        self._broker = broker

    async def publish(
        self,
        message: Any,
        routing_key: str,
        exchange: str | None = None,
    ) -> None:
        if exchange is None:
            await self._broker.publish(message, queue=routing_key)
        else:
            await self._broker.publish(message, routing_key=routing_key, exchange=exchange)