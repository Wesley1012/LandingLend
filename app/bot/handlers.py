import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from app.services.lead_service import LeadService
from app.core.config import settings

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"🤖 Я бот для приёма заявок с сайта.\n"
        f"📩 Все новые заявки будут приходить сюда.\n\n"
        f"🔗 Сайт: {settings.BASE_URL}"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📋 Доступные команды:\n"
        "/start - Приветствие\n"
        "/help - Помощь\n"
        "/stats - Статистика заявок\n"
        "/ping - Проверка работы бота"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats - статистика заявок"""
    # TODO: Подключить реальную статистику из БД
    await update.message.reply_text(
        "📊 Статистика заявок:\n\n"
        "📝 Всего заявок: 0\n"
        "📈 За сегодня: 0\n"
        "🕐 За последний час: 0"
    )


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /ping - проверка работы"""
    await update.message.reply_text("🏓 Pong! Бот работает!")


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-обработчик для текстовых сообщений (для теста)"""
    user = update.effective_user
    text = update.message.text

    await update.message.reply_text(
        f"📩 Ты написал: {text}\n\n"
        f"👤 От: {user.first_name}"
    )


# Регистрируем обработчики
def register_handlers(application):
    """Регистрирует все обработчики команд"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("ping", ping_command))

    # Эхо-обработчик для тестов (можно закомментировать)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))

    logger.info("✅ Все обработчики зарегистрированы")