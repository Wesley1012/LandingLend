from fastapi import Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging

logger = logging.getLogger(__name__)

# Создаём окружение Jinja2 без кеша
env = Environment(
    loader=FileSystemLoader("app/templates/errors/"),
    autoescape=select_autoescape(["html", "xml"]),
    cache_size=0,  # Отключаем кеш
    auto_reload=True
)
templates = Jinja2Templates(env=env)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения количества запросов"""

    # Настройки для разных эндпоинтов
    LIMITS = {
        "/": (5, 10),
        "/api/lead": (5, 30),
        "/api/lead/": (5, 30),
        "/sql_code": (10, 60),
        "/api/test": (3, 5),
    }

    DEFAULT_LIMIT = (20, 60)

    EXCLUDED_PATHS = {
        "/health",
        "/favicon.ico",
        "/sitemap.xml",
        "/robots.txt",
        # "/test",
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
            logger.warning("RateLimiter не инициализирован")
            return await call_next(request)

        rate_limiter = request.app.state.rate_limiter

        # Определяем лимиты для эндпоинта
        limit_config = self.LIMITS.get(path)
        if limit_config is None:
            for endpoint, limits in self.LIMITS.items():
                if path.startswith(endpoint):
                    limit_config = limits
                    break

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

            # Если запрос ожидает HTML (браузер) — показываем красивую страницу
            accept_header = request.headers.get("accept", "")
            if "text/html" in accept_header or path == "/":
                # Рендерим вручную
                template = templates.get_template("429.html")
                html_content = template.render({
                    "request": request,
                    "limit": max_requests,
                    "window": window_seconds,
                })
                return HTMLResponse(
                    content=html_content,
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )

            # Для API возвращаем JSON
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