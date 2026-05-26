from abc import ABC, abstractmethod
from typing import Any


class IRMQService(ABC):
    @abstractmethod
    async def publish(
        self,
        message: Any,
        routing_key: str,
        exchange: str | None = None,
    ) -> None:
        raise NotImplementedError