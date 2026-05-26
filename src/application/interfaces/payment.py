from abc import ABC, abstractmethod
from datetime import datetime

from src.core.enums import PaymentStatusEnum
from src.entities.payment import PaymentEntity
from src.application.command.payment import CreatePaymentCommand


class IPaymentRepo(ABC):

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key: str) -> PaymentEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, payment_id: int) -> PaymentEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, cmd: CreatePaymentCommand) -> PaymentEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_status(
        self,
        payment_id: int,
        status: PaymentStatusEnum,
        processed_at: datetime,
    ) -> None:
        raise NotImplementedError