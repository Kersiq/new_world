from datetime import datetime

from sqlalchemy import select, update

from src.application.command.payment import CreatePaymentCommand
from src.application.interfaces.payment import IPaymentRepo
from src.core.enums import PaymentStatusEnum
from src.persistence.db.interface import get_async_session
from src.infra.postgres.payment.model import Payment
from src.entities.payment import PaymentEntity


class PaymentRepoImpl(IPaymentRepo):
    def __init__(self, session: get_async_session):
        self.session = session

    async def get_by_idempotency_key(self, idempotency_key: str) -> PaymentEntity | None:
        stmt = select(Payment).where(Payment.idempotency_key == idempotency_key)
        result = await self.session.execute(stmt)
        row = result.scalars().first()
        return row.to_entity() if row else None

    async def get_by_id(self, payment_id: int) -> PaymentEntity | None:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(stmt)
        row = result.scalars().first()
        return row.to_entity() if row else None

    async def create(self, cmd: CreatePaymentCommand) -> PaymentEntity:
        obj = Payment(**cmd.to_dict())
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj.to_entity()

    async def update_status(
        self,
        payment_id: int,
        status: PaymentStatusEnum,
        processed_at: datetime,
    ) -> None:
        stmt = (
            update(Payment)
            .where(Payment.id == payment_id)
            .values(status=status, processed_at=processed_at)
        )
        await self.session.execute(stmt)
