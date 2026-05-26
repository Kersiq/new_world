from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime

from src.core.enums import AvailableCurrencyEnum, PaymentStatusEnum
from src.core.utils import ReturnAsDictUtils


@dataclass
class CreatePaymentCommand(ReturnAsDictUtils):
    amount: Decimal
    currency: AvailableCurrencyEnum
    description: str
    idempotency_key: str
    webhook_url: str
    processed_at: datetime | None = None
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    meta: dict = field(default_factory=dict)
