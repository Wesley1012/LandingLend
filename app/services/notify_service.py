import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_telegram_message(text: str) -> bool:
    """
    Отправляет сообщение в Telegram
    Если токен не настроен - просто логирует
    """
    # Если нет токена - просто логируем
    if not settings.TG_BOT_TOKEN or settings.TG_BOT_TOKEN == "123:ABC":
        logger.info(f"📝 [TG заглушка] Сообщение: {text}")
        return True

    try:
        import aiohttp

        url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TG_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=5) as response:
                if response.status == 200:
                    logger.info(f"✅ Сообщение в Telegram отправлено")
                    return True
                else:
                    logger.error(f"❌ Ошибка TG: {response.status}")
                    return False

    except Exception as e:
        logger.error(f"❌ Ошибка отправки в Telegram: {e}")
        return False