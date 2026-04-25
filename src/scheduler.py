import asyncio
import logging

from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.infra.services.payment import PaymentSchedulerService

logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting scheduler")
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Moscow"))

    await PaymentSchedulerService().run(scheduler)

    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
