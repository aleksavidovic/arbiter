from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .db import engine, get_db
from .redis import get_redis, redis_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Everything before yield runs on SERVER STARTUP
    yield
    # Everything after yield runs on SERVER SHUTDOWN
    await engine.dispose()
    await redis_client.aclose()

app = FastAPI(title="Arbiter", lifespan=lifespan)

DbSession = Annotated[AsyncSession, Depends(get_db)]
RedisClient = Annotated[Redis, Depends(get_redis)]

@app.get("/health")
async def health_check(db: DbSession, cache: RedisClient) -> dict[str, str]:
    await db.execute(text("SELECT 1"))

    await cache.execute_command("PING")

    return {
        "status": "ok",
        "postgres": "connected",
        "redis": "connected",
    }
