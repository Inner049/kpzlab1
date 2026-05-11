# tests/test_async_service.py
import pytest
import time
from src.services.async_demo import load_expense_data_SLOW, load_expense_data_FAST

@pytest.mark.asyncio
async def test_parallel_faster_than_sequential():
    """Перевіряємо що паралельна версія швидша"""
    t0 = time.perf_counter()
    await load_expense_data_SLOW(1)
    slow_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    await load_expense_data_FAST(1)
    fast_time = time.perf_counter() - t0

    # Паралельна версія повинна бути хоча б у 1.5 рази швидша
    assert fast_time < slow_time / 1.5, f"Очікували прискорення, але: slow={slow_time:.3f}, fast={fast_time:.3f}"

@pytest.mark.asyncio
async def test_fast_returns_all_fields():
    result = await load_expense_data_FAST(1)
    assert "expense" in result
    assert "category" in result
    assert "user" in result
