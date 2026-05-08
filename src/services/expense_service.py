# Відсутність Magic Numbers: всі константи мають назви
MAX_EXPENSE_AMOUNT = 1_000_000
MIN_EXPENSE_AMOUNT = 0.01

class ExpenseRepository:
    """SRP: Тільки робота з БД витрат"""
    def __init__(self, db_session):
        self.db = db_session
        
    def save_expense(self, user_id: int, amount: float, category_id: int):
        pass # Тут буде логіка SQLAlchemy

class NotificationService:
    """SRP: Тільки відправка сповіщень"""
    def alert_budget_exceeded(self, user_id: int):
        pass # Логіка відправки push або email

class ExpenseService:
    """SRP: Бізнес-логіка витрат"""
    # DIP: Залежності передаються через конструктор (інтерфейси)
    def __init__(self, repository: ExpenseRepository, notifier: NotificationService):
        self.repository = repository
        self.notifier = notifier

    def add_expense(self, user_id: int, amount: float, category_id: int):
        # DRY: Валідація не дублюється, використовуємо константи
        if not (MIN_EXPENSE_AMOUNT <= amount <= MAX_EXPENSE_AMOUNT):
            raise ValueError(f"Сума має бути від {MIN_EXPENSE_AMOUNT} до {MAX_EXPENSE_AMOUNT}")
            
        # Координація
        self.repository.save_expense(user_id, amount, category_id)
        
        # Перевірка бізнес-правил
        if self._is_budget_exceeded(user_id, category_id):
            self.notifier.alert_budget_exceeded(user_id)
            
        return True

    def _is_budget_exceeded(self, user_id: int, category_id: int) -> bool:
        # Логіка перевірки лімітів
        return False