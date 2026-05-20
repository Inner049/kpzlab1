"""
Unit-тести для ExpenseService
Використовують Mock для ізоляції від залежностей
"""
import pytest
from unittest.mock import Mock, patch, call
from datetime import date
from src.services.expense_service import ExpenseService
from src.exceptions import ExpenseNotFoundError, ValidationError


class TestExpenseService:
    """Unit-тести для ExpenseService з mock-залежностями"""

    def setup_method(self):
        """Налаштування перед кожним тестом"""
        self.service = ExpenseService()

    # ═══════════════════════════════════════════════════════════
    # ТЕСТИ МЕТОДУ add_expense
    # ═══════════════════════════════════════════════════════════

    @pytest.mark.unit
    def test_add_expense_saves_to_db(self):
        """Додавання витрати зберігає її в БД"""
        # Arrange
        initial_count = len(self.service.db)
        
        # Act
        new_id = self.service.add_expense(
            amount=100.0,
            category_id=1,
            description="Тест",
            expense_date=date.today()
        )
        
        # Assert
        assert len(self.service.db) == initial_count + 1
        assert new_id in self.service.db
        assert self.service.db[new_id]["amount"] == 100.0

    @pytest.mark.unit
    def test_add_expense_returns_new_id(self):
        """Додавання витрати повертає новий ID"""
        # Act
        new_id = self.service.add_expense(
            amount=200.0,
            category_id=2,
            description="Тестова витрата",
            expense_date=date.today()
        )
        
        # Assert
        assert isinstance(new_id, int)
        assert new_id > 0

    @pytest.mark.unit
    @patch('src.services.expense_service.ExpenseValidator.validate')
    def test_add_expense_validates_data(self, mock_validate):
        """Перевірка що валідатор викликається при додаванні витрати"""
        # Arrange
        amount = 150.0
        category_id = 1
        description = "Перевірка валідації"
        expense_date = date.today()
        
        # Act
        self.service.add_expense(amount, category_id, description, expense_date)
        
        # Assert — перевіряємо що validate() було викликано з правильними аргументами
        mock_validate.assert_called_once_with(amount, category_id, description, expense_date)

    @pytest.mark.unit
    @patch('src.services.expense_service.logger')
    def test_large_expense_logs_warning(self, mock_logger):
        """Витрата більше 10000 генерує WARNING лог"""
        # Act
        self.service.add_expense(
            amount=15000.0,
            category_id=1,
            description="Велика витрата",
            expense_date=date.today()
        )
        
        # Assert — перевіряємо що logger.warning() було викликано
        mock_logger.warning.assert_called_once()
        # Перевіряємо що в повідомленні є сума
        call_args = mock_logger.warning.call_args[0]
        assert "15000" in str(call_args) or 15000.0 in call_args

    @pytest.mark.unit
    @patch('src.services.expense_service.ExpenseValidator.validate')
    def test_add_expense_validation_error_propagates(self, mock_validate):
        """Якщо валідація падає — помилка пробрасується далі"""
        # Arrange — налаштовуємо mock щоб кинути ValidationError
        mock_validate.side_effect = ValidationError("amount", "Тестова помилка")
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.service.add_expense(0, 1, "Тест", date.today())
        
        assert exc_info.value.field == "amount"

    # ═══════════════════════════════════════════════════════════
    # ТЕСТИ МЕТОДУ get_expense
    # ═══════════════════════════════════════════════════════════

    @pytest.mark.unit
    def test_get_existing_expense_returns_data(self):
        """Отримання існуючої витрати повертає коректні дані"""
        # Arrange — додаємо витрату
        new_id = self.service.add_expense(
            amount=250.0,
            category_id=3,
            description="Тестова витрата для отримання",
            expense_date=date.today()
        )
        
        # Act
        expense = self.service.get_expense(new_id)
        
        # Assert
        assert expense is not None
        assert expense["amount"] == 250.0
        assert expense["category_id"] == 3

    @pytest.mark.unit
    def test_get_nonexistent_expense_raises_error(self):
        """Отримання неіснуючої витрати кидає ExpenseNotFoundError"""
        # Arrange
        nonexistent_id = 99999
        
        # Act & Assert
        with pytest.raises(ExpenseNotFoundError) as exc_info:
            self.service.get_expense(nonexistent_id)
        
        assert exc_info.value.expense_id == nonexistent_id

    @pytest.mark.unit
    @patch('src.services.expense_service.logger')
    def test_get_nonexistent_expense_logs_warning(self, mock_logger):
        """Спроба отримати неіснуючу витрату логує WARNING"""
        # Act
        try:
            self.service.get_expense(99999)
        except ExpenseNotFoundError:
            pass  # Очікувана помилка
        
        # Assert — перевіряємо що logger.warning() було викликано
        mock_logger.warning.assert_called_once()


# ═══════════════════════════════════════════════════════════
# ДОДАТКОВІ ТЕСТИ ДЛЯ ПОКРАЩЕННЯ COVERAGE
# ═══════════════════════════════════════════════════════════

class TestExpenseServiceEdgeCases:
    """Тести граничних випадків"""

    @pytest.mark.unit
    def test_service_initializes_with_sample_data(self):
        """Сервіс ініціалізується з прикладом даних"""
        service = ExpenseService()
        assert len(service.db) >= 1
        assert 1 in service.db

    @pytest.mark.unit
    @patch('src.services.expense_service.logger')
    def test_add_expense_logs_info_on_success(self, mock_logger):
        """Успішне додавання витрати логує INFO"""
        service = ExpenseService()
        service.add_expense(100, 1, "Тест", date.today())
        
        # Перевіряємо що logger.info() викликався мінімум двічі
        # (один раз на початку, один раз після успіху)
        assert mock_logger.info.call_count >= 2
