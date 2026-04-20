from dishka import Provider, Scope, provide

from src.application.interfaces.outbox_table import IOutboxRepo
from src.infra.postgres.outbox_table.repository import OutboxRepoImpl
from src.infra.postgres.payment.repository import PaymentRepoImpl
from src.application.interfaces.payment import IPaymentRepo


class RepoProvider(Provider):
    payment_repo = provide(
        source=PaymentRepoImpl,
        provides=IPaymentRepo,
        scope=Scope.REQUEST
    )

    repositories = provide(
        source=OutboxRepoImpl,
        provides=IOutboxRepo,
        scope=Scope.REQUEST
    )
