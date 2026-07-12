import redis.asyncio as redis
from typing import Optional
from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_keepalive=True
        )

    async def get_page(self, path: str) -> Optional[str]:
        """Получить закешированную страницу"""
        return await self.redis.get(f"page:{path}")

    async def set_page(self, path: str, html: str, ttl: int = 300):
        """Закешировать страницу"""
        await self.redis.setex(f"page:{path}", ttl, html)

    async def delete_page(self, path: str):
        """Инвалидировать кеш страницы"""
        await self.redis.delete(f"page:{path}")

    async def incr_metric(self, name: str) -> int:
        """Увеличить счетчик"""
        return await self.redis.incr(f"metric:{name}")

    async def get_metric(self, name: str) -> int:
        """Получить значение счетчика"""
        value = await self.redis.get(f"metric:{name}")
        return int(value) if value else 0

    async def reset_metrics(self):
        """Сбросить все счетчики (для тестов)"""
        keys = await self.redis.keys("metric:*")
        if keys:
            await self.redis.delete(*keys)

    async def health_check(self) -> bool:
        """Проверка соединения с Redis"""
        try:
            await self.redis.ping()
            return True
        except:
            return False