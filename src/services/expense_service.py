# src/services/expense_service.py
import logging
from datetime import date
from src.validators.expense_validator import ExpenseValidator
from src.exceptions import ExpenseNotFoundError

# Ініціалізуємо логер для цього модулю
logger = logging.getLogger(__name__)

class ExpenseService:
    def __init__(self):
        # Імітація БД
        self.db = {1: {"amount": 100, "category_id": 1, "description": "Кава"}}

    def add_expense(self, amount: float, category_id: int, description: str, expense_date: date):
        logger.info(f"Спроба додати нову витрату: {amount} UAH") # 1. INFO
        try:
            logger.debug(f"Валідація даних: amount={amount}, cat={category_id}") # 2. DEBUG
            ExpenseValidator.validate(amount, category_id, description, expense_date)
            
            if amount > 10000:
                logger.warning(f"Увага: додається незвично велика витрата: {amount}") # 3. WARNING

            new_id = len(self.db) + 1
            self.db[new_id] = {"amount": amount, "category_id": category_id, "description": description}
            
            logger.info(f"Витрату успішно збережено з ID {new_id}") # 4. INFO
            return new_id
        except Exception as e:
            logger.error(f"Помилка при збереженні витрати: {e}", exc_info=True) # 5. ERROR
            raise

    def get_expense(self, expense_id: int):
        logger.debug(f"Пошук витрати ID {expense_id}")
        if expense_id not in self.db:
            logger.warning(f"Витрату ID {expense_id} не знайдено!")
            raise ExpenseNotFoundError(expense_id)
        return self.db[expense_id]