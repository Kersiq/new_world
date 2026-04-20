from decimal import Decimal

from pydantic import BaseModel

from src.core.enums import AvailableCurrencyEnum


class PostPaymentRequest(BaseModel):
    amount: Decimal
    currency: AvailableCurrencyEnum
    description: str
    metadata: str
    webhook_url: str
