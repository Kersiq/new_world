from pydantic import BaseModel

from datetime import datetime

from src.core.enums import PaymentStatusEnum

class PostPaymentResponse(BaseModel):
    payment_id: str
    status: PaymentStatusEnum
    created_at: datetime