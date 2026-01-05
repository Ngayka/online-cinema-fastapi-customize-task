import redis.asyncio as redis
from src.config.dependencies import get_settings


settings = get_settings()

redis_client: redis.Redis | None = None


async def setup_redis():
    global redis_client

    redis_client = redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )
