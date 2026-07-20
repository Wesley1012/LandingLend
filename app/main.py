from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import main, lead, seo
from app.middleware import SecurityHeadersMiddleware, RateLimitMiddleware
from app.core.config import settings
from app.core.rate_limiter import lifespan
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
    lifespan=lifespan
)

# CORS — должен быть первым
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [settings.BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter — после CORS, до остальных
app.add_middleware(RateLimitMiddleware)

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
    try:
        redis = app.state.redis
        await redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )