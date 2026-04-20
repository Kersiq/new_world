from pydantic import BaseModel

from datetime import datetime

class PostPaymentResponse(BaseModel):
    payment_id: str
    status: PaymentStatusEnum
    created_at: datetime