import logging
from typing import Any

from dishka import AsyncContainer
from faststream.rabbit import RabbitBroker, RabbitMessage, RabbitRouter

from src.application.usecases.process_payment import ProcessPaymentUseCase
from src.core.config import config
from src.persistence.rmq.rmq_init import payments_exchange, payments_new_queue

logger = logging.getLogger(__name__)


def make_payments_router(container: AsyncContainer, broker: RabbitBroker) -> RabbitRouter:
    router = RabbitRouter()

    @router.subscriber(payments_new_queue(), payments_exchange())
    async def handle_payment(payload: dict[str, Any], msg: RabbitMessage) -> None:
        x_death = msg.headers.get("x-death") or []
        attempts = x_death[0].get("count", 0) if x_death else 0

        if attempts >= config.rabbit.max_retries:
            logger.warning(
                "Payment exceeded retries (%s), moving to DLQ. payload=%s",
                attempts, payload,
            )
            await broker.publish(
                payload,
                routing_key=config.rabbit.payments_dlq,
                exchange=config.rabbit.payments_exchange,
            )
            return

        payment_id = payload.get("payment_id")
        webhook_url = payload.get("webhook_url", "")

        if not isinstance(payment_id, int):
            logger.error("Invalid payload, missing payment_id: %s", payload)
            return

        async with container() as request_container:
            uc = await request_container.get(ProcessPaymentUseCase)
            await uc.execute(payment_id=payment_id, webhook_url=webhook_url)

    return router
