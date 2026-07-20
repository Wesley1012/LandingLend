from fastapi import APIRouter, Form, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.services.cache_service import CacheService
from app.services.lead_service import LeadService
from app.services.notify_service import send_telegram_message

router = APIRouter(prefix="/api", tags=["leads"])


@router.post("/lead")
async def create_lead(
        request: Request,
        background_tasks: BackgroundTasks,
        name: str = Form(...),
        phone: str = Form(...),
        cache: CacheService = Depends(),
):
    """Обработка заявки с формы"""

    print(f"Получены данные: name={name}, phone={phone}")

    lead_id = await LeadService.save_lead(name, phone)
    await cache.incr_metric("leads")

    background_tasks.add_task(
        send_telegram_message,
        f"🔔 <b>Новая заявка!</b>\n\n"
        f"👤 Имя: {name}\n"
        f"📱 Телефон: {phone}\n"
        f"🆔 ID: {lead_id}"
    )

    return JSONResponse({
        "ok": True,
        "lead_id": lead_id,
        "message": "Заявка успешно отправлена!"
    })