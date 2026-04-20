from dataclasses import dataclass
from datetime import datetime

from src.core.enums import PaymentStatusEnum


@dataclass
class PaymentInfoDTO:
    id: str
    status: PaymentStatusEnum
    created_at: datetime