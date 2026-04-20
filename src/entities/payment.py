from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

from src.core.enums import AvailableCurrencyEnum, PaymentStatusEnum


@dataclass
class PaymentEntity:
    id: int
    amount: Decimal
    currency: AvailableCurrencyEnum
    description: str
    meta: dict
    status: PaymentStatusEnum
    idempotency_key: str
    webhook_url: str
    processed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None