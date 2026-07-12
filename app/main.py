from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import main, lead, seo
from app.middleware import SecurityHeadersMiddleware
from app.core.config import settings
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version="1.0.0"
)

# CORS (настройте под свой домен)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [settings.BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Безопасность и SEO заголовки
app.add_middleware(SecurityHeadersMiddleware)

# Статика
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Роуты
app.include_router(main.router)
app.include_router(lead.router)
app.include_router(seo.router)

# Health check
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "debug": settings.DEBUG
    }

# Запуск
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )