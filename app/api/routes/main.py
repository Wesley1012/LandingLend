from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.services.cache_service import CacheService
from app.services.seo_service import get_home_seo
from app.core.security import generate_csrf_token
from app.core.config import settings

router = APIRouter()

# Настройка Jinja2 без кеша
env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"]),
    cache_size=0,
    auto_reload=True
)
templates = Jinja2Templates(env=env)


@router.get("/")
async def index(
        request: Request,
        cache: CacheService = Depends()
):
    """Главная страница с SEO"""

    seo_data = get_home_seo()
    views = await cache.get_metric("views") or 0
    leads = await cache.get_metric("leads") or 0

    context = {
        "request": request,
        "seo_data": seo_data.get_meta_tags(request),
        "csrf_token": generate_csrf_token(),
        "views_count": views,
        "leads_count": leads,
        "debug": settings.DEBUG
    }

    await cache.incr_metric("views")

    template = templates.get_template("index.html")
    html_content = template.render(context)

    return HTMLResponse(content=html_content)


@router.get("/test")
async def test_endpoint():
    """Тестовый эндпоинт для проверки работы API"""
    return {"status": "ok", "message": "Server is working!"}