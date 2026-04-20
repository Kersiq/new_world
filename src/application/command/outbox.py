from dataclasses import dataclass
from datetime import datetime
from src.core.enums import OutboxEventTypes, OutboxStatusEnum


@dataclass
class CreateOutboxCommand:
    routing_key:str
    payload: dict
    event_id: str
    last_error: str
    next_retry_at: datetime
    attempts: int = 0
    status: OutboxStatusEnum = OutboxStatusEnum.PENDING
    event_type: OutboxEventTypes = OutboxEventTypes.PAYMENT
