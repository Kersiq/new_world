from abc import ABC, abstractmethod
from typing import Any


class IRMQService(ABC):
    @abstractmethod
    async def publish(self, message: Any, queue: str) -> None:
        raise NotImplementedError