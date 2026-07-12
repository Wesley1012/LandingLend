from fastapi import APIRouter, Form, Request, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

from app.services.cache_service import CacheService
from app.services.lead_service import LeadService
from app.services.notify_service import send_telegram_message
from app.core.security import verify_csrf_token

router = APIRouter(prefix="/api", tags=["leads"])


# Pydantic модель для валидации
class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    csrf_token: str = Field(default="")

    @validator('phone')
    def validate_phone(cls, v):
        # Убираем все нецифровые символы для проверки
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError('Номер телефона должен содержать минимум 10 цифр')
        return v


@router.post("/lead")
async def create_lead(
        request: Request,
        background_tasks: BackgroundTasks,
        lead_data: LeadCreate = Depends(),
        cache: CacheService = Depends(),
):
    """Обработка заявки с формы"""

    # Проверка CSRF (пока отключена для тестов)
    # if lead_data.csrf_token:
    #     if not verify_csrf_token(lead_data.csrf_token, request.cookies.get("csrf_token")):
    #         raise HTTPException(status_code=403, detail="Bad CSRF token")

    # Сохраняем заявку
    lead_id = await LeadService.save_lead(lead_data.name, lead_data.phone)

    # Счетчик заявок в Redis
    await cache.incr_metric("leads")

    # Отправляем в Telegram в фоне
    background_tasks.add_task(
        send_telegram_message,
        f"🔔 Новая заявка с лендинга!\n\n👤 Имя: {lead_data.name}\n📱 Телефон: {lead_data.phone}\n🆔 ID: {lead_id}"
    )

    return JSONResponse({
        "ok": True,
        "lead_id": lead_id,
        "message": "Заявка успешно отправлена!"
    })