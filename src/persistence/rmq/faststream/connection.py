from faststream.rabbit import RabbitBroker

from src.core.config import config
from src.application.interfaces.services.i_rmq import IRMQService
from src.infra.rmq.service.faststream_rmq import FastStreamRMQService
from src.persistence.rmq.faststream.interface import get_rabbit_broker


async def rabbit_broker_impl() -> RabbitBroker:
    broker = RabbitBroker(config.rabbit.get_dsn())
    await broker.start()
    return broker


async def rmq_service_impl(
    broker: get_rabbit_broker,
) -> IRMQService:
    return FastStreamRMQService(broker)