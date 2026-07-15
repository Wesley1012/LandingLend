#!/usr/bin/env python
import asyncio
import logging
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.bot import application
from app.bot.handlers import register_handlers

logging.basicConfig(level=logging.INFO)


async def main():
    """Запуск бота"""
    # Регистрируем обработчики
    register_handlers(application)

    # Запускаем бота
    print("🚀 Бот запускается...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("✅ Бот успешно запущен и работает!")

    try:
        # Бесконечное ожидание
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("⏹️ Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⏹️ Бот остановлен")