from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from app.core.config import settings


@dataclass
class SeoData:
    """SEO данные для страницы"""
    title: str
    description: str
    keywords: str = ""
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: str = "/static/img/og-image.jpg"
    og_type: str = "website"
    canonical: Optional[str] = None
    robots: str = "index, follow"

    def __post_init__(self):
        if self.og_title is None:
            self.og_title = self.title
        if self.og_description is None:
            self.og_description = self.description
        if self.canonical is None:
            self.canonical = "/"

    def get_meta_tags(self, request) -> Dict[str, Any]:
        """Генерирует все мета-теги для шаблона"""
        url = f"{settings.BASE_URL}{request.url.path}"

        return {
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "og_title": self.og_title,
            "og_description": self.og_description,
            "og_image": f"{settings.BASE_URL}{self.og_image}",
            "og_url": url,
            "og_type": self.og_type,
            "canonical": f"{settings.BASE_URL}{self.canonical}",
            "robots": self.robots,
            "site_name": settings.SITE_NAME
        }


# ===== SEO для главной страницы =====
def get_home_seo() -> SeoData:
    return SeoData(
        title="Разработка лендингов на FastAPI — Создание сайтов-визиток",
        description="Создаём крутые лендинги на FastAPI с Telegram-ботами, SEO-оптимизацией, админ-панелью и мониторингом. Индивидуальный подход, поддержка 1 месяц.",
        keywords="разработка лендингов, создание сайтов-визиток, fastapi разработка, telegram бот для сайта, seo оптимизация, админ панель для сайта",
        og_title="LandPr — Разработка лендингов на FastAPI",
        og_description="Создаём сайты-визитки с Telegram-ботами, SEO и админ-панелью. Быстро, качественно, с поддержкой."
    )


# ===== SEO для услуг =====
def get_telegram_bot_seo() -> SeoData:
    return SeoData(
        title="Разработка Telegram ботов для сайтов — Интеграция с лендингом",
        description="Создание и интеграция Telegram ботов для лендингов. Уведомления о заявках, интерактивные кнопки, рассылки. Настройка под ваш бизнес.",
        keywords="telegram бот для сайта, интеграция телеграм бота, уведомления в телеграм, бот для лендинга",
        og_title="Telegram бот для лендинга — Разработка и интеграция",
        og_description="Интегрируем Telegram бота с вашим сайтом. Уведомления, кнопки, автоматизация."
    )


def get_seo_seo() -> SeoData:
    return SeoData(
        title="SEO-оптимизация лендингов — Настройка под поисковые системы",
        description="Комплексная SEO-настройка лендингов: мета-теги, микроразметка Schema.org, sitemap, robots.txt, подключение аналитики.",
        keywords="seo оптимизация лендинга, настройка seo, микроразметка сайта, schema.org, seo для сайта-визитки",
        og_title="SEO-оптимизация лендингов — Вывод в ТОП",
        og_description="Настраиваем SEO для вашего лендинга: мета-теги, микроразметка, sitemap, аналитика."
    )


def get_admin_panel_seo() -> SeoData:
    return SeoData(
        title="Админ-панель для лендинга — Управление контентом и заявками",
        description="Удобная админ-панель для лендинга: просмотр заявок, управление контентом, статистика и графики. Интуитивный интерфейс.",
        keywords="админ панель для сайта, управление лендингом, просмотр заявок, административная панель",
        og_title="Админ-панель для лендинга — Управление сайтом",
        og_description="Полноценная админ-панель для управления лендингом. Заявки, контент, статистика."
    )


def get_design_seo() -> SeoData:
    return SeoData(
        title="Дизайн лендингов на заказ — Уникальный дизайн сайтов-визиток",
        description="Разработка уникального дизайна лендингов под ваш бренд. UI/UX-аудит, адаптивная вёрстка, современные тренды.",
        keywords="дизайн лендинга, заказать дизайн сайта, уникальный дизайн, ui ux дизайн, адаптивная верстка",
        og_title="Дизайн лендингов на заказ — Индивидуальный подход",
        og_description="Создаём уникальный дизайн лендингов под ваш бренд. Современно, красиво, эффективно."
    )


def get_parser_seo() -> SeoData:
    return SeoData(
        title="Парсеры данных для сайтов — Сбор и обработка информации",
        description="Разработка парсеров для сбора данных с сайтов. Мониторинг цен, сбор контактов, автоматизация рутинных задач.",
        keywords="парсер данных, сбор информации с сайтов, мониторинг цен, автоматизация сбора данных",
        og_title="Парсеры данных — Сбор и автоматизация",
        og_description="Разрабатываем парсеры для сбора данных с сайтов. Мониторинг, контакты, выгрузка."
    )


def get_full_complex_seo() -> SeoData:
    return SeoData(
        title="Полный комплекс разработки лендинга — Всё под ключ",
        description="Полный цикл разработки лендинга: дизайн, вёрстка, бэкенд, Telegram-бот, SEO, админ-панель. Поддержка 1 месяц в подарок.",
        keywords="разработка лендинга под ключ, комплексная разработка сайта, сайт-визитка, fastapi разработка",
        og_title="Разработка лендинга под ключ — Полный комплекс",
        og_description="Всё включено: дизайн, разработка, бот, SEO, админка. Поддержка 1 месяц."
    )


# ===== SEO для страницы контактов (если добавите) =====
def get_contacts_seo() -> SeoData:
    return SeoData(
        title="Контакты — Разработка лендингов на FastAPI",
        description="Свяжитесь с нами для заказа разработки лендинга. Telegram, почта, телефон — мы на связи 24/7.",
        keywords="контакты разработчика лендингов, заказать лендинг, разработка сайтов",
        og_title="Контакты — LandPr",
        og_description="Свяжитесь с нами для заказа разработки лендинга."
    )


# ===== Фабрика для динамических страниц =====
def get_service_seo(service_name: str, service_desc: str) -> SeoData:
    """SEO для динамических страниц услуг"""
    return SeoData(
        title=f"{service_name} — Разработка лендингов на FastAPI | LandPr",
        description=f"{service_desc}. Закажите разработку лендинга с индивидуальным подходом и поддержкой 1 месяц.",
        keywords=f"{service_name}, разработка лендингов, fastapi, создание сайтов"
    )