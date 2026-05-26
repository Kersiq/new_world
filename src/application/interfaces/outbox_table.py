from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence


from src.application.command.outbox import CreateOutboxCommand
from src.core.enums import OutboxEventTypes
from src.entities.outbox_table import OutboxEntity


class IOutboxRepo(ABC):

    @abstractmethod
    async def create(self, cmd: CreateOutboxCommand) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_pending(self, event_type: OutboxEventTypes) -> list[OutboxEntity]:
        raise NotImplementedError

    @abstractmethod
    async def mark_as_sent(self, ids: Sequence[int]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def increment_attempt(
        self, event_id: int, error: str, next_retry_at: datetime
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def mark_as_failed(self, event_id: int, error: str) -> None:
        raise NotImplementedError