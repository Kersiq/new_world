import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.infra.postgres.base import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_table"

    event_type: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False)
    payload: Mapped[dict] = mapped_column(sa.JSON, nullable=False)
    routing_key: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False)
    status: Mapped[str] = mapped_column(
        sa.VARCHAR(20), default="pending", nullable=False
    )
    attempts: Mapped[int] = mapped_column(sa.INTEGER, default=0, nullable=False)
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(sa.DateTime(timezone=True))
    last_error: Mapped[Optional[str]] = mapped_column(sa.TEXT)
    event_id: Mapped[UUID] = mapped_column(sa.UUID, unique=True, nullable=False)