"""
Модуль для роботи з витратами.
Містить бізнес-логіку для додавання та отримання фінансових записів.
"""
import logging
from datetime import date
from src.validators.expense_validator import ExpenseValidator
from src.exceptions import ExpenseNotFoundError

# Ініціалізуємо логер для цього модулю
logger = logging.getLogger(__name__)


class ExpenseService:
    """Сервіс для управління фінансовими витратами."""

    def __init__(self):
        """Ініціалізація сервісу з імітацією бази даних."""
        # Імітація БД
        self.db = {1: {"amount": 100, "category_id": 1, "description": "Кава"}}

    def add_expense(
        self, amount: float, category_id: int, description: str, expense_date: date
    ):
        """
        Додає нову витрату до бази даних.

        Args:
            amount (float): Сума витрати.
            category_id (int): ID категорії.
            description (str): Опис витрати.
            expense_date (date): Дата витрати.

        Returns:
            int: ID нової збереженої витрати.
        """
        logger.info("Спроба додати нову витрату: %s UAH", amount)  # 1. INFO
        try:
            logger.debug(
                "Валідація даних: amount=%s, cat=%s", amount, category_id
            )  # 2. DEBUG
            ExpenseValidator.validate(amount, category_id, description, expense_date)

            if amount > 10000:
                logger.warning(
                    "Увага: додається незвично велика витрата: %s", amount
                )  # 3. WARNING

            new_id = len(self.db) + 1
            self.db[new_id] = {
                "amount": amount,
                "category_id": category_id,
                "description": description
            }

            logger.info("Витрату успішно збережено з ID %s", new_id)  # 4. INFO
            return new_id
        except Exception as e:
            logger.error(
                "Помилка при збереженні витрати: %s", e, exc_info=True
            )  # 5. ERROR
            raise

    def get_expense(self, expense_id: int):
        """
        Отримує дані про витрату за її ідентифікатором.

        Args:
            expense_id (int): Ідентифікатор витрати.

        Returns:
            dict: Словник з даними про витрату.

        Raises:
            ExpenseNotFoundError: Якщо витрату з таким ID не знайдено.
        """
        logger.debug("Пошук витрати ID %s", expense_id)
        if expense_id not in self.db:
            logger.warning("Витрату ID %s не знайдено!", expense_id)
            raise ExpenseNotFoundError(expense_id)
        return self.db[expense_id]