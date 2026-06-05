import time
from fastapi import Depends, FastAPI, Request, Response
from fastapi.security import HTTPBearer
from src.api import router
from src.database.db import init_db
from fastapi import  Request, Response


security = HTTPBearer(auto_error=False)

app = FastAPI(dependencies=[Depends(security)])

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


@app.middleware("http")
async def test_middleware(request: Request, call_next) -> Response:
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()
    process_time = (end_time - start_time) * 1000

    print(f"{request.method} {request.url.path} - {process_time:.0f}ms")

    return response
