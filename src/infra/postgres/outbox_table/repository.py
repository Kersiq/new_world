from datetime import datetime
from sqlalchemy import select, update

from src.application.interfaces.outbox_table import IOutboxRepo
from src.core.enums import OutboxStatusEnum
from src.infra.postgres.outbox_table.model import OutboxEvent
from src.persistence.db.interface import get_async_session
from src.application.command.outbox import CreateOutboxCommand


class OutboxRepoImpl(IOutboxRepo):
    def __init__(self, session: get_async_session):
        self.session = session

    async def create(self, cmd: CreateOutboxCommand) -> None:
        obj = OutboxEvent(
            **cmd.to_dict()
        )
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

    async def get_pending(self) -> list[OutboxEvent]:
        stmt = (
            select(OutboxEvent)
            .where(
                OutboxEvent.status == OutboxStatusEnum.PENDING,
            )
            .with_for_update(skip_locked=True)
        ).limit(10)

        result = await self.session.execute(stmt)
        result = result.scalars().all()
        return [model.to_entity() for model in result]

    async def mark_as_sent(self, ids: list[int]) -> None:
        stmt = (
            update(OutboxEvent)
            .where(OutboxEvent.id.in_(ids))
            .values(status=OutboxStatusEnum.SENT)
        )

        await self.session.execute(stmt)
        await self.session.commit()
