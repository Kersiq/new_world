from abc import ABC, abstractmethod


from src.application.command.outbox import CreateOutboxCommand


class IOutboxRepo(ABC):
    @abstractmethod
    async def create(self, cmd: CreateOutboxCommand) -> None:
        raise NotImplementedError
