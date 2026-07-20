from contextlib import asynccontextmanager
from functools import lru_cache
from redis.asyncio import Redis
from time import time
import random
from fastapi import FastAPI, HTTPException, status, Request, Body
from fastapi.responses import JSONResponse


@lru_cache
def get_redis() -> Redis:
    """Получаем подключение к Redis (кэшируем)"""
    from app.core.config import settings
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


class RateLimiter:
    """Лимитер запросов на основе Redis"""

    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_limited(
            self,
            ip_address: str,
            endpoint: str,
            max_requests: int,
            window_seconds: int,
    ) -> bool:
        """Проверяет, не превышен ли лимит запросов"""
        key = f"rate_limiter:{endpoint}:{ip_address}"

        current_ms = time() * 1000
        window_start_ms = current_ms - window_seconds * 1000
        current_request = f"{time() * 1000}-{random.randint(0, 100_000)}"

        async with self._redis.pipeline() as pipe:
            await pipe.zremrangebyscore(key, 0, window_start_ms)
            await pipe.zcard(key)
            await pipe.zadd(key, {current_request: current_ms})
            await pipe.expire(key, window_seconds)

            res = await pipe.execute()

        _, current_count, _, _ = res
        return current_count >= max_requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan для управления Redis"""
    redis = get_redis()
    try:
        await redis.ping()
        print("Redis работает")
        app.state.redis = redis
        app.state.rate_limiter = RateLimiter(redis)
        yield
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        raise
    finally:
        await redis.aclose()
        print("Redis отключен")