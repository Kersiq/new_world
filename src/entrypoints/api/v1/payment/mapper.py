from src.application.command.payment import CreatePaymentCommand
from src.entrypoints.api.v1.payment.requests import PostPaymentRequest


class PaymentMapper:

    @staticmethod
    def create_payment_request_to_command(
            schema: PostPaymentRequest, ik: str
    ) -> CreatePaymentCommand:
        return CreatePaymentCommand(
            amount=schema.amount,
            currency=schema.currency,
            webhook_url=schema.webhook_url,
            meta=schema.metadata,
            description=schema.description,
            processed_at=None,
            idempotency_key=ik
        )
