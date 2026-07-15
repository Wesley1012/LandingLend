import logging
from telegram import Bot
from telegram.ext import Application
from app.core.config import settings

logger = logging.getLogger(__name__)


def create_bot():
    """Создаёт экземпляр бота с поддержкой прокси"""

    # Базовый URL для обхода блокировок (BotGate)
    base_url = getattr(settings, 'TG_API_BASE_URL', None)

    if base_url:
        from telegram.request import HTTPXRequest
        request = HTTPXRequest()
        bot = Bot(
            token=settings.TG_BOT_TOKEN,
            base_url=f"{base_url}/bot",
            request=request
        )
        logger.info(f"✅ Бот использует кастомный URL: {base_url}")
    else:
        bot = Bot(token=settings.TG_BOT_TOKEN)
        logger.info("✅ Бот использует стандартный API Telegram")

    return bot


# Создаём экземпляр бота
bot = create_bot()

# Создаём приложение
application = Application.builder().token(settings.TG_BOT_TOKEN).build()