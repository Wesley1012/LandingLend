from fastapi import APIRouter, Request, Response
from app.core.config import settings

router = APIRouter()


@router.get("/sitemap.xml")
async def sitemap(request: Request):
    """Динамическая карта сайта для поисковиков"""
    base_url = settings.BASE_URL
    today = "2026-07-11"  # В реальном проекте - datetime.now().date()

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{base_url}/menu</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/prices</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/contacts</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>"""

    return Response(
        content=sitemap_content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@router.get("/robots.txt")
async def robots():
    """Robots.txt для управления индексацией"""
    base_url = settings.BASE_URL
    content = f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /static/
Disallow: /health

Sitemap: {base_url}/sitemap.xml

# Яндекс
Host: {base_url.replace('https://', '')}

# Общие правила
Crawl-delay: 1
"""
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Cache-Control": "public, max-age=86400"}  # Кеш на сутки
    )