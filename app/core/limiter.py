# app/core/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from starlette.responses import JSONResponse
# slowapi is a wrapper around the limits package to make it work nicely with FastAPI/Starlette.
# limits is the underlying Python library that actually implements rate-limiting logic (counters, storage backends like Redis, Memcached, in-memory, etc.).
from limits.storage import RedisStorage

## Python in-memory
# Create a limiter instance (using client IP as the key)
limiter = Limiter(key_func=get_remote_address)


## Redis backend memory
# storage = RedisStorage("redis://localhost:6379")
# limiter = Limiter(key_func=get_remote_address, storage=storage)


# Custom rate limit exceeded response
def rate_limit_exceeded_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": f"Rate limit exceeded: {exc.detail}"
        },
    )


# In-memory storage (default)
# Stores counters inside the Python process memory.
# Works only if you have one FastAPI process (not good for multi-worker production).
# If app restarts → counters reset.
# Redis storage (recommended)
# Stores counters in Redis (centralized).
# Works across multiple workers / multiple servers.
# Survives restarts.
# Ideal for production.
