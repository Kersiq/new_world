from faststream.rabbit import RabbitBroker
from src.application.interfaces.services.i_rmq import IRMQService


def get_rabbit_broker() -> RabbitBroker:
    raise NotImplementedError


def get_rmq_service() -> IRMQService:
    raise NotImplementedError