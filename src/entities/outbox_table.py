from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.enums import OutboxEventTypes, OutboxStatusEnum


@dataclass
class OutboxEntity:
    id: int
    updated_at: datetime
    created_at: datetime
    event_type: OutboxEventTypes
    payload: dict
    routing_key: str
    status: OutboxStatusEnum
    attempts: int
    next_retry_at: datetime
    last_error: str
    event_id: UUID
