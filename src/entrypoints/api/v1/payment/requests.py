from decimal import Decimal

from pydantic import BaseModel

from src.core.enums import AvailableCurrencyEnum


class PostPaymentRequest(BaseModel):
    amount: Decimal
    currency: AvailableCurrencyEnum
    description: str
    metadata: dict
    webhook_url: str
