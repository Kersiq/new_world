import logging
import asyncio

from src.application.interfaces.outbox_table import IOutboxRepo
from src.application.interfaces.services.i_rmq import IRMQService
from src.core.config import config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

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
        pending_tasks = await self.outbox_repo.get_pending()

        if not pending_tasks:
            logger.info("No pending outbox tasks found")
            return

        async def publish(task):
            try:
                await self.rabbit.publish(
                    task.payload,
                    config.rabbit.payment_process,
                )
                return task.id
            except Exception as e:
                logger.exception(f"Failed to publish task {task.id}: {e}")
                return None

        results = await asyncio.gather(
            *(publish(task) for task in pending_tasks),
            return_exceptions=False,
        )

        succeeded_ids = [task_id for task_id in results if task_id is not None]

        if succeeded_ids:
            await self.outbox_repo.mark_as_sent(succeeded_ids)
            logger.info(f"Published {len(succeeded_ids)} outbox events")