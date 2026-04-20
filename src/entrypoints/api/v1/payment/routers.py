from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, status

from src.entrypoints.api.v1.payment.requests import PostPaymentRequest
from src.entrypoints.api.v1.payment.responses import PostPaymentResponse


router = APIRouter(
    prefix="/payments",
    tags=["Onboarding / V1"],
    route_class=DishkaRoute,
)


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=PostPaymentResponse)
async def post_request_payment(
        data: PostPaymentRequest,
        uc: FromDishka[None],
) -> PostPaymentResponse:
