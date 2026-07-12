import pytest
from app.core.security import generate_csrf_token, verify_csrf_token


def test_generate_csrf_token():
    """Тест генерации CSRF токена"""
    token1 = generate_csrf_token()
    token2 = generate_csrf_token()

    assert token1 is not None
    assert token2 is not None
    assert token1 != token2
    assert len(token1) == 64  # 32 байта в HEX = 64 символа


def test_verify_csrf_token():
    """Тест проверки CSRF токена"""
    token = generate_csrf_token()

    assert verify_csrf_token(token, token) is True
    assert verify_csrf_token(token, "wrong") is False
    assert verify_csrf_token(None, token) is False
    assert verify_csrf_token(token, None) is False


def test_csrf_token_security():
    """Тест, что токены непредсказуемы"""
    tokens = [generate_csrf_token() for _ in range(100)]
    # Все токены должны быть уникальными
    assert len(set(tokens)) == len(tokens)