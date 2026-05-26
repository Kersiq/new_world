import logging
import asyncio

from src.application.interfaces.outbox_table import IOutboxRepo
from src.application.interfaces.services.i_rmq import IRMQService
from src.core.config import config
from src.core.enums import OutboxEventTypes


logger = logging.getLogger(__name__)


class ProducePaymentIntoRMQUseCase:
    def __init__(
        self,
        rabbit: IRMQService,
        outbox_repo: IOutboxRepo,
    ) -> None:
        self.rabbit = rabbit
        self.outbox_repo = outbox_repo

    async def execute(self) -> None:
        pending_tasks = await self.outbox_repo.get_pending(OutboxEventTypes.PAYMENT)

        if not pending_tasks:
            logger.info("No pending payment outbox tasks found")
            return

        async def publish(task):
            try:
                await self.rabbit.publish(
                    task.payload,
                    routing_key=config.rabbit.payments_new,
                    exchange=config.rabbit.payments_exchange,
                )
                return task.id
            except Exception:
                logger.exception("Failed to publish task %s", task.id)
                return None

        results = await asyncio.gather(
            *(publish(task) for task in pending_tasks),
            return_exceptions=False,
        )

        succeeded_ids = [task_id for task_id in results if task_id is not None]

        if succeeded_ids:
            await self.outbox_repo.mark_as_sent(succeeded_ids)
            logger.info("Published %s outbox events", len(succeeded_ids))