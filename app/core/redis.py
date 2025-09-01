import redis.asyncio as redis
from functools import lru_cache
from fastapi import Depends

class RedisClient:
    def __init__(self, url: str = "redis://localhost:6379/0"):
        self._url = url
        self._client: redis.Redis | None = None

    async def get_client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.from_url(self._url, decode_responses=True)
        return self._client


# Singleton-style usage
@lru_cache
def get_redis_client() -> RedisClient:
    return RedisClient()

# we often use it for global config so the object is created only once:
# What is @lru_cache and How It Works?
# @lru_cache is from Python’s functools.
# LRU = Least Recently Used.
# It caches function results in memory (not Redis).
