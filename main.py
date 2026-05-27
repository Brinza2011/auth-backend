import time

from fastapi import FastAPI, Request, Response

from src.api import router
from src.database.db import init_db

app = FastAPI()

app.include_router(router)


@app.middleware("http")
async def test_middleware(request: Request, call_next) -> Response:
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()
    print(f"Request took {end_time - start_time} seconds")

    return response


@app.on_event("startup")
async def startup():
    await init_db()
