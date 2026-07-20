from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения количества запросов"""

    # Настройки для разных эндпоинтов
    LIMITS = {
        "/": (5, 10),  # 5 запросов в 10 секунд на главную
        "/api/lead": (5, 30),  # 5 запросов в 30 секунд
        "/api/lead/": (5, 30),
        "/sql_code": (10, 60),  # 10 запросов в минуту
        "/api/test": (3, 5),  # 3 запроса в 5 секунд
    }

    # Лимит по умолчанию: 20 запросов в минуту
    DEFAULT_LIMIT = (20, 60)

    # Эндпоинты, которые не лимитируем
    EXCLUDED_PATHS = {
        "/health",
        "/favicon.ico",
        "/sitemap.xml",
        "/robots.txt",
        "/test",
        "/cache-status",
        "/static",
    }

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Пропускаем исключения
        if path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # Пропускаем статику
        if path.startswith("/static/") or path.startswith("/.well-known/"):
            return await call_next(request)

        # Получаем IP клиента
        client_ip = request.client.host if request.client else "unknown"

        # Проверяем, есть ли лимитер в состоянии приложения
        if not hasattr(request.app.state, 'rate_limiter'):
            logger.warning("⚠️ RateLimiter не инициализирован")
            return await call_next(request)

        rate_limiter = request.app.state.rate_limiter

        # Определяем лимиты для эндпоинта
        # Проверяем точное совпадение, а затем частичное
        limit_config = self.LIMITS.get(path)
        if limit_config is None:
            # Проверяем, не начинается ли путь с какого-то эндпоинта
            for endpoint, limits in self.LIMITS.items():
                if path.startswith(endpoint):
                    limit_config = limits
                    break

        # Если не нашли, используем дефолтный
        if limit_config is None:
            limit_config = self.DEFAULT_LIMIT

        max_requests, window_seconds = limit_config

        # Проверяем лимит
        is_limited = await rate_limiter.is_limited(
            ip_address=client_ip,
            endpoint=path,
            max_requests=max_requests,
            window_seconds=window_seconds
        )

        if is_limited:
            logger.warning(f"Rate limit exceeded: {client_ip} -> {path} ({max_requests}/{window_seconds}s)")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "limit": max_requests,
                    "window": window_seconds,
                    "message": f"Превышен лимит: {max_requests} запросов за {window_seconds} секунд"
                }
            )

        response = await call_next(request)
        return response