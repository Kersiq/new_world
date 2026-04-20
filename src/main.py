import uvicorn
from fastapi import FastAPI, APIRouter

from dishka.integrations.fastapi import setup_dishka


from src.core.config import config
from src.entrypoints.api import v1_router
from src.di import get_async_container

app = FastAPI()

main_router = APIRouter()
app.include_router(v1_router)

def init_di(app_: FastAPI):
    container = get_async_container()
    app_.container = container
    setup_dishka(container, app_)


if __name__ == '__main__':
    uvicorn.run(app, host=config.web.host, port=config.web.port)
