from fastapi import FastAPI
from src.api import router
from src.database.db import init_db

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    await init_db()

