from datetime import datetime, timedelta

from uuid_extensions import uuid7

from src.application.command.outbox import CreateOutboxCommand
from src.application.command.payment import CreatePaymentCommand
from src.application.interfaces.outbox_table import IOutboxRepo
from src.application.interfaces.payment import IPaymentRepo
from src.application.usecases.check_idempotency_key_use_case import CheckPaymentIdempotencyKeyUseCase
from src.infra.postgres.payment.dto import PaymentInfoDTO


class CreatePaymentUseCase:
    def __init__(
            self,
            check_payment_by_idem_k_uc: CheckPaymentIdempotencyKeyUseCase,
            payment_repo: IPaymentRepo,
            outbox_repo: IOutboxRepo
    ) -> None:
        self.check_payment_by_idem_k_uc = check_payment_by_idem_k_uc
        self.payment_repo = payment_repo
        self.outbox_repo = outbox_repo

    async def execute(self, cmd: CreatePaymentCommand, ik: str) -> PaymentInfoDTO:
        check_payment = await self.check_payment_by_idem_k_uc.execute(ik)
        if check_payment:
            return check_payment

        new_payment = await self.payment_repo.create(
            cmd
        )
        await self.outbox_repo.create(
            CreateOutboxCommand(
                routing_key="payment.created",
                payload={
                    "amount": str(cmd.amount),
                    "currency": cmd.currency.value,
                    "description": cmd.description,
                    "idempotency_key": cmd.idempotency_key,
                    "webhook_url": cmd.webhook_url,
                    "status": cmd.status.value,
                    "meta": cmd.meta,
                },
                event_id=str(uuid7()),
                last_error="",
                next_retry_at=datetime.utcnow() + timedelta(seconds=10),
            )
        )

        return new_payment
