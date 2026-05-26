from abc import ABC, abstractmethod

from src.entities.payment import PaymentEntity
from src.application.command.payment import CreatePaymentCommand


class IPaymentRepo(ABC):

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key: str) -> PaymentEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, cmd: CreatePaymentCommand) -> PaymentEntity:
        raise NotImplementedError