from dishka import Provider, Scope, provide

from src.infra.postgres.payment.repository import PaymentRepoImpl
from src.application.interfaces.payment import IPaymentRepo


class RepoProvider(Provider):
    payment_repo = provide(
        source=PaymentRepoImpl,
        provides=IPaymentRepo,
        scope=Scope.REQUEST
    )
