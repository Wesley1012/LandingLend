import pytest
from tests.conftest import MockCacheService


@pytest.mark.asyncio
async def test_cache_set_get():
    """Тест установки и получения из кеша"""
    cache = MockCacheService()

    await cache.set_page("test", "Hello World", ttl=10)
    result = await cache.get_page("test")

    assert result == "Hello World"


@pytest.mark.asyncio
async def test_cache_delete():
    """Тест удаления из кеша"""
    cache = MockCacheService()

    await cache.set_page("test", "Hello")
    await cache.delete_page("test")
    result = await cache.get_page("test")

    assert result is None


@pytest.mark.asyncio
async def test_metrics():
    """Тест счетчиков метрик"""
    cache = MockCacheService()

    await cache.incr_metric("views")
    views = await cache.get_metric("views")
    assert views == 1

    await cache.incr_metric("views")
    views = await cache.get_metric("views")
    assert views == 2


@pytest.mark.asyncio
async def test_health_check():
    """Тест проверки здоровья"""
    cache = MockCacheService()
    result = await cache.health_check()
    assert result is True