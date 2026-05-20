"""
Калькулятор для підрахунку витрат
Створено через TDD (Test-Driven Development)
"""
from typing import List, Dict, Any
from datetime import date


def calculate_monthly_total(user_expenses: List[Dict[str, Any]], month: int, year: int) -> float:
    """
    Підраховує загальну суму витрат за конкретний місяць.
    
    Args:
        user_expenses: Список витрат, кожна витрата має ключі 'amount' (float) та 'date' (date)
        month: Номер місяця (1-12)
        year: Рік (наприклад, 2026)
    
    Returns:
        float: Загальна сума витрат за вказаний місяць
    
    Raises:
        ValueError: Якщо month не в діапазоні 1-12
    
    Example:
        >>> from datetime import date
        >>> expenses = [
        ...     {"amount": 100.0, "date": date(2026, 5, 1)},
        ...     {"amount": 200.0, "date": date(2026, 5, 15)},
        ... ]
        >>> calculate_monthly_total(expenses, 5, 2026)
        300.0
    """
    # Валідація вхідних параметрів
    if not 1 <= month <= 12:
        raise ValueError("Місяць має бути від 1 до 12")
    
    # Підрахунок суми через list comprehension (більш Pythonic)
    return sum(
        expense["amount"]
        for expense in user_expenses
        if expense["date"].month == month and expense["date"].year == year
    )
