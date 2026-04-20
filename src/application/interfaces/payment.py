from abc import ABC, abstractmethod


from src.infra.postgres.payment.dto import PaymentInfoDTO
from src.application.command.payment import CreatePaymentCommand


class IPaymentRepo(ABC):

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key) -> PaymentInfoDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, cmd: CreatePaymentCommand) -> PaymentInfoDTO | None:
        raise NotImplementedError