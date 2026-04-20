from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka

from src.entrypoints.api import v1_router
from src.di import get_async_container


def init_di(app_: FastAPI):
    container = get_async_container()
    app_.container = container
    setup_dishka(container, app_)


def create_app() -> FastAPI:
    app_ = FastAPI()
    app_.include_router(v1_router)
    init_di(app_)
    return app_

app = create_app()
