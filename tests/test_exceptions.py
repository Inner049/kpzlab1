# tests/test_exceptions.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.exceptions import ValidationError, ExpenseNotFoundError, AppError

def test_validation_error_has_field():
    err = ValidationError("amount", "Сума некоректна")
    assert err.field == "amount"
    assert "amount" in str(err)

def test_expense_not_found_dict():
    err = ExpenseNotFoundError(99)
    d = err.to_dict()
    assert d["error"] == "EXPENSE_NOT_FOUND"
    assert "99" in d["message"]

def test_business_error_hierarchy():
    err = ExpenseNotFoundError(1)
    assert isinstance(err, AppError)  # Перевірка ієрархії

# --- ЗАВДАННЯ ДЛЯ ЗАКРІПЛЕННЯ 10.1 (@retry) ---
import random
import time
import functools

def retry(max_attempts=3, delay=0.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"[RETRY] Помилка: {e}. Спроба {attempt}/{max_attempts}...")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
def unstable_request(url: str) -> dict:
    if random.random() < 0.6:  # 60% шанс на помилку
        raise ConnectionError("Тимчасово недоступно")
    return {"status": "ok", "url": url}

if __name__ == "__main__":
    test_validation_error_has_field()
    test_expense_not_found_dict()
    test_business_error_hierarchy()
    print("Всі 3 тести на exceptions пройдено!\n")
    
    print("--- Демонстрація @retry ---")
    try:
        res = unstable_request("http://api.expensetracker.com/sync")
        print("Запит успішний:", res)
    except Exception as e:
        print("Запит повністю провалився:", e)
