import pytest
from fastapi.testclient import TestClient


def test_create_lead_success(client: TestClient):
    """Тест успешного создания заявки"""
    data = {
        "name": "Иван Тестов",
        "phone": "+7 999 123-45-67",
        "csrf_token": "test_token"
    }

    response = client.post("/api/lead", data=data)

    # Должен быть успех, т.к. CSRF отключен в тестах
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "lead_id" in data


def test_create_lead_missing_name(client: TestClient):
    """Тест отправки формы без имени"""
    data = {
        "phone": "+7 999 123-45-67",
        "csrf_token": "test_token"
    }

    response = client.post("/api/lead", data=data)
    assert response.status_code == 422  # FastAPI валидация


def test_create_lead_missing_phone(client: TestClient):
    """Тест отправки формы без телефона"""
    data = {
        "name": "Иван",
        "csrf_token": "test_token"
    }

    response = client.post("/api/lead", data=data)
    assert response.status_code == 422


def test_create_lead_invalid_name(client: TestClient):
    """Тест с слишком коротким именем (если есть валидация)"""
    data = {
        "name": "A",
        "phone": "+7 999 123-45-67",
        "csrf_token": "test_token"
    }

    response = client.post("/api/lead", data=data)
    # FastAPI валидирует min_length=2
    assert response.status_code == 422


def test_create_lead_with_csrf_disabled(client: TestClient):
    """Тест формы без CSRF (когда защита отключена)"""
    data = {
        "name": "Тест",
        "phone": "+7 999 123-45-67"
    }

    response = client.post("/api/lead", data=data)
    # CSRF отключен, должно пройти
    assert response.status_code == 200