from redis.asyncio import Redis

from .config import settings

redis_client: Redis = Redis.from_url(
    str(settings.redis_dsn),
    decode_responses=True,
)

async def get_redis() -> Redis:
    return redis_client

