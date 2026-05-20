"""
Калькулятор для підрахунку витрат
Створено через TDD (Test-Driven Development)
"""


def calculate_monthly_total(user_expenses: list, month: int, year: int) -> float:
    """
    Підраховує загальну суму витрат за конкретний місяць.
    
    Args:
        user_expenses: Список витрат, кожна витрата має ключ 'amount' та 'date'
        month: Номер місяця (1-12)
        year: Рік (наприклад, 2026)
    
    Returns:
        float: Загальна сума витрат за вказаний місяць
    
    Raises:
        ValueError: Якщо month не в діапазоні 1-12
    
    Example:
        >>> expenses = [
        ...     {"amount": 100.0, "date": date(2026, 5, 1)},
        ...     {"amount": 200.0, "date": date(2026, 5, 15)},
        ... ]
        >>> calculate_monthly_total(expenses, 5, 2026)
        300.0
    """
    # Валідація місяця
    if not 1 <= month <= 12:
        raise ValueError("Місяць має бути від 1 до 12")
    
    # Підрахунок суми
    total = 0.0
    for expense in user_expenses:
        expense_date = expense["date"]
        if expense_date.month == month and expense_date.year == year:
            total += expense["amount"]
    
    return total
