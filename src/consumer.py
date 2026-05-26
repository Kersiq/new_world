import asyncio
import logging

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.core.config import config
from src.di import get_async_container
from src.entrypoints.consumers.payment_consumer import make_payments_router
from src.persistence.rmq.rmq_init import declare_payments_topology

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    container = get_async_container()
    broker = RabbitBroker(config.rabbit.get_dsn())
    broker.include_router(make_payments_router(container, broker))

    app = FastStream(broker)

    @app.after_startup
    async def declare_topology() -> None:
        await declare_payments_topology(broker)
        logger.info("Payments topology declared")

    logger.info("Starting payment consumer")
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
