from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.application.usecases.scheduler.add_payment_into_rmq import ProducePaymentIntoRMQUseCase
from src.di import get_async_container

class PaymentSchedulerService:
    def __init__(
        self,
        produce_payment_tasks: ProducePaymentIntoRMQUseCase = ProducePaymentIntoRMQUseCase,
    ) -> None:
        self._produce_payment_tasks = produce_payment_tasks

    @staticmethod
    async def __run_cron_with_container(uc, flag: bool | None = None) -> None:
        container = get_async_container()
        async with container() as cont:
            uc = await cont.get(uc)
            if flag is not None:
                uc.execute(flag)
            else:
                await uc.execute()

    async def run(self, scheduler: AsyncIOScheduler) -> None:
        scheduler_time = "* * * * *"

        scheduler.add_job(
            self.__run_cron_with_container,
            args=[self._produce_payment_tasks],
            trigger=CronTrigger.from_crontab(
                scheduler_time
            ),
            id="_produce_payment_tasks",
            coalesce=True,
            max_instances=1,
            replace_existing=True,
        )

