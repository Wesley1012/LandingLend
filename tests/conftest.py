import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.cache_service import CacheService


class MockCacheService:
    """Мок для CacheService (без Redis)"""

    def __init__(self):
        self._cache = {}
        self._metrics = {}

    async def get_page(self, path: str):
        return self._cache.get(f"page:{path}")

    async def set_page(self, path: str, html: str, ttl: int = 300):
        self._cache[f"page:{path}"] = html

    async def delete_page(self, path: str):
        self._cache.pop(f"page:{path}", None)

    async def incr_metric(self, name: str) -> int:
        key = f"metric:{name}"
        self._metrics[key] = self._metrics.get(key, 0) + 1
        return self._metrics[key]

    async def get_metric(self, name: str) -> int:
        return self._metrics.get(f"metric:{name}", 0)

    async def health_check(self) -> bool:
        return True


@pytest.fixture
def client():
    """Тестовый клиент FastAPI с моком CacheService"""

    # Переопределяем зависимость для тестов
    def override_cache():
        return MockCacheService()

    app.dependency_overrides[CacheService] = override_cache

    with TestClient(app) as test_client:
        yield test_client

    # Очищаем после тестов
    app.dependency_overrides.clear()


@pytest.fixture
def mock_cache():
    """Мок для CacheService"""
    return MockCacheService()


@pytest.fixture
def sample_lead_data():
    """Тестовые данные заявки"""
    return {
        "name": "Тест Тестов",
        "phone": "+7 999 123-45-67"
    }