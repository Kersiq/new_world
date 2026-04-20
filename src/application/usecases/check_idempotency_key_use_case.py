from src.application.interfaces.payment import IPaymentRepo
from src.infra.postgres.payment.dto import PaymentInfoDTO


class CheckPaymentIdempotencyKeyUseCase:
    def __init__(
            self,
            payment_repo: IPaymentRepo
    ) -> None:
        self.payment_repo = payment_repo

    async def execute(
            self,
            idempotency_key: str
    ) -> PaymentInfoDTO | None:
        payment_exist = await self.payment_repo.get_by_idempotency_key(
            idempotency_key=idempotency_key
        )
        return payment_exist


