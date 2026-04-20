from abc import ABC, abstractmethod


from src.infra.postgres.payment.dto import PaymentInfoDTO


class IPaymentRepo(ABC):

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key) -> PaymentInfoDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, cmd: CreatePaymentCommand) -> int:
        raise NotImplementedError