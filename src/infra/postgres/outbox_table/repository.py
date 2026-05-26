from datetime import datetime, UTC

from sqlalchemy import or_, select, update

from src.application.interfaces.outbox_table import IOutboxRepo
from src.core.enums import OutboxEventTypes, OutboxStatusEnum
from src.infra.postgres.outbox_table.model import OutboxEvent
from src.persistence.db.interface import get_async_session
from src.application.command.outbox import CreateOutboxCommand


class OutboxRepoImpl(IOutboxRepo):
    def __init__(self, session: get_async_session):
        self.session = session

    async def create(self, cmd: CreateOutboxCommand) -> None:
        obj = OutboxEvent(**cmd.to_dict())
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

    async def get_pending(self, event_type: OutboxEventTypes) -> list[OutboxEvent]:
        now = datetime.now(UTC)
        stmt = (
            select(OutboxEvent)
            .where(
                OutboxEvent.status == OutboxStatusEnum.PENDING,
                OutboxEvent.event_type == event_type,
                or_(
                    OutboxEvent.next_retry_at.is_(None),
                    OutboxEvent.next_retry_at <= now,
                ),
            )
            .with_for_update(skip_locked=True)
            .limit(10)
        )

        result = await self.session.execute(stmt)
        return [model.to_entity() for model in result.scalars().all()]

    async def mark_as_sent(self, ids: list[int]) -> None:
        stmt = (
            update(OutboxEvent)
            .where(OutboxEvent.id.in_(ids))
            .values(status=OutboxStatusEnum.SENT)
        )
        await self.session.execute(stmt)

    async def increment_attempt(
        self, event_id: int, error: str, next_retry_at: datetime
    ) -> None:
        stmt = (
            update(OutboxEvent)
            .where(OutboxEvent.id == event_id)
            .values(
                attempts=OutboxEvent.attempts + 1,
                last_error=error,
                next_retry_at=next_retry_at,
            )
        )
        await self.session.execute(stmt)

    async def mark_as_failed(self, event_id: int, error: str) -> None:
        stmt = (
            update(OutboxEvent)
            .where(OutboxEvent.id == event_id)
            .values(
                status=OutboxStatusEnum.FAILED,
                attempts=OutboxEvent.attempts + 1,
                last_error=error,
            )
        )
        await self.session.execute(stmt)
