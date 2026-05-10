# src/exceptions.py
class AppError(Exception):
    """Базовий клас для всіх помилок застосунку"""
    def __init__(self, message: str, code: str = "APP_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self):
        """Для зручного повернення помилок в JSON API"""
        return {"error": self.code, "message": self.message}

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        super().__init__(f"Помилка в полі '{field}': {message}", code="VALIDATION_ERROR")
        self.field = field

    def to_dict(self):
        d = super().to_dict()
        d["field"] = self.field
        return d

# --- Бізнес-помилки (мінімум 3) ---
class ExpenseNotFoundError(AppError):
    def __init__(self, expense_id: int):
        super().__init__(f"Витрату з ID {expense_id} не знайдено", code="EXPENSE_NOT_FOUND")
        self.expense_id = expense_id

class CategoryNotFoundError(AppError):
    def __init__(self, category_id: int):
        super().__init__(f"Категорію з ID {category_id} не знайдено", code="CATEGORY_NOT_FOUND")
        self.category_id = category_id

class BudgetExceededError(AppError):
    def __init__(self, category: str, amount: float, limit: float):
        super().__init__(f"Бюджет для '{category}' перевищено! Спроба: {amount}, Ліміт: {limit}", code="BUDGET_EXCEEDED")
