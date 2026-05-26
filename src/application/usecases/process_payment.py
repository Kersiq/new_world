import asyncio
import logging
import random
from datetime import datetime, UTC

from uuid_extensions import uuid7

from src.application.command.outbox import CreateOutboxCommand
from src.application.interfaces.outbox_table import IOutboxRepo
from src.application.interfaces.payment import IPaymentRepo
from src.core.enums import OutboxEventTypes, PaymentStatusEnum

logger = logging.getLogger(__name__)


class PaymentGatewayError(Exception):
    pass


class ProcessPaymentUseCase:
    def __init__(
        self,
        payment_repo: IPaymentRepo,
        outbox_repo: IOutboxRepo,
    ) -> None:
        self.payment_repo = payment_repo
        self.outbox_repo = outbox_repo

    async def execute(self, payment_id: int, webhook_url: str) -> None:
        payment = await self.payment_repo.get_by_id(payment_id)
        if payment is None:
            logger.warning("Payment %s not found, skip", payment_id)
            return
        if payment.status != PaymentStatusEnum.PENDING:
            logger.info("Payment %s already processed (status=%s)", payment_id, payment.status)
            return

        await asyncio.sleep(random.uniform(2.0, 5.0))

        if random.random() < 0.1:
            new_status = PaymentStatusEnum.FAILED
            logger.info("Payment %s failed by gateway", payment_id)
        else:
            new_status = PaymentStatusEnum.SUCCEEDED
            logger.info("Payment %s succeeded", payment_id)

        processed_at = datetime.now(UTC)
        await self.payment_repo.update_status(payment_id, new_status, processed_at)

        await self.outbox_repo.create(
            CreateOutboxCommand(
                routing_key="webhook.delivery",
                payload={
                    "payment_id": payment_id,
                    "status": new_status.value,
                    "webhook_url": webhook_url,
                    "processed_at": processed_at.isoformat(),
                },
                event_id=str(uuid7()),
                last_error="",
                next_retry_at=processed_at,
                event_type=OutboxEventTypes.WEBHOOK_DELIVERY,
            )
        )
