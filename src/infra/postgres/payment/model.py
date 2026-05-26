import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from decimal import Decimal

from src.core.enums import AvailableCurrencyEnum, PaymentStatusEnum
from src.infra.postgres.base import Base
from src.entities.payment import PaymentEntity


class Payment(Base):
    __tablename__ = 'payment'

    amount: Mapped[Decimal] = mapped_column(sa.DECIMAL)
    currency: Mapped[AvailableCurrencyEnum] = mapped_column(sa.VARCHAR(255))
    description: Mapped[str] = mapped_column(sa.TEXT)
    meta: Mapped[dict] = mapped_column(sa.JSON)
    status: Mapped[PaymentStatusEnum] = mapped_column(sa.VARCHAR(20))
    idempotency_key: Mapped[str] = mapped_column(sa.UUID, unique=True) #could be uuid7
    webhook_url: Mapped[str] = mapped_column(sa.VARCHAR)
    processed_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)

    def to_entity(self) -> PaymentEntity:
        return PaymentEntity(
            id=self.id,
            amount=self.amount,
            currency=self.currency,
            description=self.description,
            meta=self.meta,
            status=self.status,
            idempotency_key=self.idempotency_key,
            webhook_url=self.webhook_url,
            processed_at=self.processed_at,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
