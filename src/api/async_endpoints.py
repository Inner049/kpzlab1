# src/api/async_endpoints.py
import asyncio
import logging
import aiohttp
from src.services.async_demo import load_expense_data_FAST

logger = logging.getLogger(__name__)

# --- Фонова задача (КРОК 4) ---
async def background_export_report(user_id: int):
    """Ця задача працює у фоні і не блокує відповідь користуачу"""
    logger.info("Початок фонової генерації звіту для user_id=%s", user_id)
    await asyncio.sleep(2.0) # Імітація довгої роботи (генерація PDF)
    logger.info("Фонова генерація звіту ЗАВЕРШЕНА для user_id=%s", user_id)

# --- Async Ендпоінт (КРОК 3) ---
async def get_expense_details_endpoint(expense_id: int, user_id: int):
    """Ендпоінт, що збирає дані паралельно і запускає фонову задачу"""
    
    # 1. Паралельна вибірка даних (Швидко)
    data = await load_expense_data_FAST(expense_id)
    
    # 2. Запуск фонової задачі (не чекаємо на її завершення)
    asyncio.create_task(background_export_report(user_id))
    
    # 3. Миттєво повертаємо результат
    return {"status": "success", "data": data, "message": "Звіт генерується у фоні"}

# --- Завдання для закріплення 12.1 (Retry з Exponential Backoff) ---
async def fetch_with_retry(url: str, max_attempts: int = 3) -> dict:
    for attempt in range(1, max_attempts + 1):
        try:
            async with aiohttp.ClientSession() as session:
                # Встановлюємо таймаут 3 секунди
                async with session.get(url, timeout=3.0) as response:
                    response.raise_for_status()
                    return await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            logger.warning("Спроба %s провалилась: %s", attempt, e)
            if attempt == max_attempts:
                raise
            delay = 2 ** (attempt - 1) # 1s, 2s, 4s...
            await asyncio.sleep(delay)
