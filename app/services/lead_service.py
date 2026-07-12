import uuid
from datetime import datetime
from typing import Optional


class LeadService:
    """Сервис для работы с заявками"""

    @staticmethod
    async def save_lead(name: str, phone: str) -> str:
        """
        Сохраняет заявку в БД (пока заглушка)
        В будущем заменим на реальную работу с PostgreSQL
        """
        lead_id = str(uuid.uuid4())[:8]

        # TODO: Сохранять в базу данных
        print(f"[{datetime.now()}] Заявка #{lead_id}: {name} - {phone}")

        # Имитация асинхронной задержки
        import asyncio
        await asyncio.sleep(0.1)

        return lead_id

    @staticmethod
    async def get_lead(lead_id: str) -> Optional[dict]:
        """Получить заявку по ID (заглушка)"""
        # TODO: Реализовать получение из БД
        return {
            "id": lead_id,
            "name": "Тест",
            "phone": "+7 999 123-45-67",
            "created_at": datetime.now().isoformat()
        }

    @staticmethod
    async def get_all_leads(limit: int = 100) -> list:
        """Получить все заявки (заглушка)"""
        # TODO: Реализовать получение из БД
        return [
            {
                "id": "123",
                "name": "Иван",
                "phone": "+7 999 123-45-67",
                "created_at": datetime.now().isoformat()
            }
        ]