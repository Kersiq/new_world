from dishka import Provider, Scope, provide

from src.application.usecases.check_idempotency_key_use_case import CheckPaymentIdempotencyKeyUseCase
from src.application.usecases.create_payment import CreatePaymentUseCase


class UseCaseProvider(Provider):
    check_payment_by_ik_provider = provide(
        source=CheckPaymentIdempotencyKeyUseCase,
        scope=Scope.REQUEST
    )
    create_payment_uc = provide(
        source=CreatePaymentUseCase,
        scope=Scope.REQUEST
    )