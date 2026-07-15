import aiohttp
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_telegram_message(text: str, chat_id: str = None) -> bool:
    """Отправляет сообщение в Telegram через Bot API"""

    if not settings.TG_BOT_TOKEN or settings.TG_BOT_TOKEN == "123:ABC":
        logger.warning("⚠️ TG_BOT_TOKEN не настроен")
        return False

    # Если chat_id не передан, используем из настроек
    if chat_id is None:
        chat_id = settings.TG_CHAT_ID

    # Базовый URL с поддержкой BotGate
    base_url = getattr(settings, 'TG_API_BASE_URL', 'https://api.telegram.org')
    url = f"{base_url}/bot{settings.TG_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as response:
                if response.status == 200:
                    logger.info("✅ Сообщение в Telegram отправлено")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Ошибка TG: {response.status} - {error_text}")
                    return False
    except Exception as e:
        logger.error(f"❌ Ошибка отправки в Telegram: {e}")
        return False