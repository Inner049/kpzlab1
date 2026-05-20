"""
Спільні fixtures для всіх тестів
"""
import pytest
import sqlite3
from datetime import date


@pytest.fixture
def in_memory_db():
    """
    Створює SQLite базу даних в пам'яті для інтеграційних тестів.
    Після завершення тесту — автоматично закривається.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def sample_expense_data():
    """
    Повертає приклад коректних даних для витрати.
    Використовується в багатьох тестах.
    """
    return {
        "amount": 150.50,
        "category_id": 1,
        "description": "Кава в кафе",
        "expense_date": date.today()
    }


@pytest.fixture
def sample_expenses_list():
    """
    Повертає список витрат для тестування функцій агрегації.
    """
    return [
        {"amount": 100.0, "date": date(2026, 5, 1), "category_id": 1},
        {"amount": 200.0, "date": date(2026, 5, 15), "category_id": 2},
        {"amount": 50.0, "date": date(2026, 6, 1), "category_id": 1},
        {"amount": 75.0, "date": date(2026, 5, 20), "category_id": 3},
    ]
