import pytest
from fastapi.testclient import TestClient

def test_home_page_status(client: TestClient):
    """Проверка, что главная страница доступна"""
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_content(client: TestClient):
    """Проверка контента главной страницы"""
    response = client.get("/")
    assert response.status_code == 200

    # Проверяем наличие ключевых элементов
    assert "Шаурма" in response.text
    assert "Преимущества" in response.text
    assert "Заказать звонок" in response.text

    # Проверяем логотип (можно по частям)
    assert "Land" in response.text and "Pr" in response.text

def test_test_endpoint(client: TestClient):
    """Проверка тестового эндпоинта"""
    response = client.get("/test")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Server is working!" in data["message"]

def test_health_check(client: TestClient):
    """Проверка health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data

def test_seo_meta_tags(client: TestClient):
    """Проверка SEO мета-тегов"""
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>" in response.text
    assert "description" in response.text
    assert "og:title" in response.text

def test_sitemap(client: TestClient):
    """Проверка sitemap.xml"""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "<?xml" in response.text
    assert "urlset" in response.text

def test_robots(client: TestClient):
    """Проверка robots.txt"""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent" in response.text
    assert "Sitemap" in response.text