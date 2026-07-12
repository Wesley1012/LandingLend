import secrets
from fastapi import Request, Response

def generate_csrf_token() -> str:
    """Генерирует CSRF токен для защиты форм"""
    return secrets.token_hex(32)

def verify_csrf_token(token: str, cookie_token: str) -> bool:
    """Проверяет CSRF токен (сравнивает с токеном из cookie)"""
    if not token or not cookie_token:
        return False
    # Сравниваем токен из формы и из cookie (двойная отправка)
    return secrets.compare_digest(token, cookie_token)

def set_secure_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: int = 3600,
    httponly: bool = True,
    secure: bool = False,  # В разработке False, в продакшене True
    samesite: str = "lax"
) -> None:
    """Устанавливает безопасную Cookie"""
    response.set_cookie(
        key=key,
        value=value,
        httponly=httponly,
        secure=secure,
        samesite=samesite,
        max_age=max_age,
    )