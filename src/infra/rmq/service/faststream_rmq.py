from typing import Any

from src.application.interfaces.services.i_rmq import IRMQService
from src.persistence.rmq.faststream.interface import get_rabbit_broker


class FastStreamRMQService(IRMQService):
    def __init__(self, broker: get_rabbit_broker):
        self._broker = broker

    async def publish(self, message: Any, queue: str) -> None:
        await self._broker.publish(message, queue=queue)