from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Добавляет заголовки безопасности и SEO-заголовки"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        # Безопасность
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # HSTS (только в HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # SEO: Время загрузки страницы
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Response-Time"] = f"{process_time:.0f}ms"

        # Кеширование для статики
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=86400"

        return response