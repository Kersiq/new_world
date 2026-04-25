from abc import ABC, abstractmethod
from typing import Sequence


from src.application.command.outbox import CreateOutboxCommand
from src.entities.outbox_table import OutboxEntity


class IOutboxRepo(ABC):

    @abstractmethod
    async def create(self, cmd: CreateOutboxCommand) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_pending(self) -> list[OutboxEntity]:
        raise NotImplementedError

    @abstractmethod
    async def mark_as_sent(self, ids: Sequence[int]) -> None:
        raise NotImplementedError