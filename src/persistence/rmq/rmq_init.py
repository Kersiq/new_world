from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue, ExchangeType

from src.core.config import config


def _payments_exchange() -> RabbitExchange:
    return RabbitExchange(
        config.rabbit.payments_exchange,
        type=ExchangeType.DIRECT,
        durable=True,
    )


def _payments_new_queue() -> RabbitQueue:
    return RabbitQueue(
        config.rabbit.payments_new,
        durable=True,
        routing_key=config.rabbit.payments_new,
        arguments={
            "x-dead-letter-exchange": config.rabbit.payments_exchange,
            "x-dead-letter-routing-key": config.rabbit.payments_retry,
        },
    )


def _payments_retry_queue() -> RabbitQueue:
    return RabbitQueue(
        config.rabbit.payments_retry,
        durable=True,
        routing_key=config.rabbit.payments_retry,
        arguments={
            "x-message-ttl": config.rabbit.retry_ttl_ms,
            "x-dead-letter-exchange": config.rabbit.payments_exchange,
            "x-dead-letter-routing-key": config.rabbit.payments_new,
        },
    )


def _payments_dlq_queue() -> RabbitQueue:
    return RabbitQueue(
        config.rabbit.payments_dlq,
        durable=True,
        routing_key=config.rabbit.payments_dlq,
    )


async def declare_payments_topology(broker: RabbitBroker) -> None:
    exchange = await broker.declare_exchange(_payments_exchange())
    for queue in (_payments_new_queue(), _payments_retry_queue(), _payments_dlq_queue()):
        rmq_queue = await broker.declare_queue(queue)
        await rmq_queue.bind(exchange, routing_key=queue.routing_key)


def payments_new_queue() -> RabbitQueue:
    return _payments_new_queue()


def payments_exchange() -> RabbitExchange:
    return _payments_exchange()
