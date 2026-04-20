from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Depends, Header
from fastapi.security import APIKeyHeader

from src.application.usecases.create_payment import CreatePaymentUseCase
from src.entrypoints.api.v1.payment.mapper import PaymentMapper
from src.entrypoints.api.v1.payment.requests import PostPaymentRequest
from src.entrypoints.api.v1.payment.responses import PostPaymentResponse


x_api_key_dependency = APIKeyHeader(name="X-API-Key", auto_error=False)

router = APIRouter(
    prefix="/payments",
    tags=["Onboarding / V1"],
    route_class=DishkaRoute,
    dependencies=[Depends(x_api_key_dependency)],
)

@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=PostPaymentResponse)
async def post_request_payment(
        data: PostPaymentRequest,

        uc: FromDishka[CreatePaymentUseCase],
        idempotency_key: str = Header(..., alias="Idempotency-Key"),
) -> PostPaymentResponse:

    result = await uc.execute(PaymentMapper.create_payment_request_to_command(
        data, idempotency_key,
    ))
    return PaymentMapper.create_payment_entity_to_response(
        result,
    )
