

from sqlalchemy import select

from src.application.interfaces.outbox_table import IOutboxRepo
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

