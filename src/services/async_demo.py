# src/services/async_demo.py
import asyncio
import time

async def simulate_db_query(table: str, id: int, delay: float = 0.2) -> dict:
    """Імітація асинхронного запиту до БД"""
    await asyncio.sleep(delay)
    return {"table": table, "id": id, "data": f"Дані з {table}[{id}]"}

async def load_expense_data_SLOW(expense_id: int) -> dict:
    """ПОВІЛЬНО: послідовні запити"""
    expense = await simulate_db_query("expenses", expense_id, 0.3)
    category = await simulate_db_query("categories", expense_id, 0.2)
    user = await simulate_db_query("users", expense_id, 0.15)
    return {"expense": expense, "category": category, "user": user}

async def load_expense_data_FAST(expense_id: int) -> dict:
    """ШВИДКО: паралельні запити через gather"""
    expense, category, user = await asyncio.gather(
        simulate_db_query("expenses", expense_id, 0.3),
        simulate_db_query("categories", expense_id, 0.2),
        simulate_db_query("users", expense_id, 0.15),
    )
    return {"expense": expense, "category": category, "user": user}

async def benchmark():
    print("Порівняння: Sequential vs Parallel (Expense Tracker)")
    
    t0 = time.perf_counter()
    await load_expense_data_SLOW(1)
    t1 = time.perf_counter()
    
    await load_expense_data_FAST(1)
    t2 = time.perf_counter()

    print(f"Послідовно:  {t1-t0:.3f} сек")
    print(f"Паралельно:  {t2-t1:.3f} сек")
    print(f"Прискорення: {(t1-t0)/(t2-t1):.1f}x")

if __name__ == "__main__":
    asyncio.run(benchmark())
