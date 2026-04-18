import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid_extensions import uuid7
from datetime import datetime
from decimal import Decimal

from src.infra.postgres.base import Base


class Payment(Base):
    __tablename__ = 'payment'

    amount: Mapped[Decimal] = mapped_column(sa.DECIMAL)
    currency: Mapped[str] = mapped_column(sa.VARCHAR(255))
    description: Mapped[str] = mapped_column(sa.TEXT)
    meta: Mapped[dict] = mapped_column(sa.JSON)
    status: Mapped[str] = mapped_column(sa.VARCHAR(20))
    Idempotency_key: Mapped[str] = mapped_column(sa.UUID) #could be uuid7
    webhook_url: Mapped[str] = mapped_column(sa.VARCHAR)
    processed_at: Mapped[datetime | None]
