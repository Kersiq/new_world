

from sqlalchemy import select

from src.application.command.payment import CreatePaymentCommand
from src.application.interfaces.payment import IPaymentRepo
from src.infra.postgres.payment.dto import PaymentInfoDTO
from src.persistence.db.interface import get_async_session
from src.infra.postgres.payment.model import Payment
from src.entities.payment import PaymentEntity


class PaymentRepoImpl(IPaymentRepo):
    def __init__(self, session: get_async_session):
        self.session = session

    async def get_by_idempotency_key(self, idempotency_key: str) -> PaymentInfoDTO:
        stmt = select(Payment.id, Payment.status, Payment.created_at).where(
            Payment.idempotency_key == idempotency_key
        )
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        return PaymentInfoDTO(
            id=result.id,
            status=result.status,
            created_at=result.created_at,
        ) if result else None

    async def create(self, cmd: CreatePaymentCommand) -> PaymentEntity:
        obj = Payment(
            **cmd.to_dict()
        )
        await self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj.to_entity()

