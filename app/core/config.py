import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME : str = "Cool Landing"
    DEBUG : bool = False
    SECRET_KEY : str = os.getenv("SECRET_KEY")

    BASE_URL: str = "https://test-domain.com"

    REDIS_URL: str = "redis://localhost:6379"

    # База данных (опционально)
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # Telegram
    TG_BOT_TOKEN: str = "123:ABC"
    TG_CHAT_ID: str = "-100123456"

    # SEO
    SITE_NAME: str = "LandingLend"
    SITE_DESCRIPTION: str = "Разработка сайтов-визиток для любого бизнеса"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()