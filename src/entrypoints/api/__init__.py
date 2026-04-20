from fastapi import APIRouter

from src.entrypoints.api.v1.payment.routers import router as payment_router


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(payment_router)