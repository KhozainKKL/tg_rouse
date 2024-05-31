from contextlib import asynccontextmanager

import uvicorn
from environs import Env
from fastapi import FastAPI

from bot.run import bot
from core.models import Base, db_helper
from fastapi.middleware.cors import CORSMiddleware
from api_v1 import router as router_v1

from core.config import settings
from telebot.async_telebot import asyncio_helper

env = Env()
env.read_env()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":

    uvicorn.run("main:app", port=8080, reload=True)
