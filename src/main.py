import uvicorn
from fastapi import FastAPI
from core.config import config

app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(app, host=config.web.host, port=config.web.port)
