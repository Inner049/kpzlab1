# src/validators/expense_validator.py
from datetime import date
from src.exceptions import ValidationError

class ExpenseValidator:
    ALLOWED_CATEGORIES = [1, 2, 3, 4, 5]

    @staticmethod
    def validate(amount: float, category_id: int, description: str, expense_date: date):
        if amount <= 0:
            raise ValidationError("amount", "Сума має бути більшою за нуль")
        if amount > 1_000_000:
            raise ValidationError("amount", "Сума перевищує ліміт системи")
        
        if category_id not in ExpenseValidator.ALLOWED_CATEGORIES:
            raise ValidationError("category_id", f"Категорія {category_id} недопустима")
        
        if not description or len(description.strip()) < 3:
            raise ValidationError("description", "Опис занадто короткий (мінімум 3 символи)")
        
        if expense_date > date.today():
            raise ValidationError("expense_date", "Дата витрати не може бути в майбутньому")
