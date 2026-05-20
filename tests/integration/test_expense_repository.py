"""
Інтеграційні тести для ExpenseRepository
Використовують реальну SQLite БД в пам'яті
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from datetime import date
from src.repositories.expense_repo import ExpenseRepository


class TestExpenseRepositoryIntegration:
    """Інтеграційні тести з реальною БД"""

    @pytest.mark.integration
    def test_save_and_find_expense(self, in_memory_db):
        """Зберегти витрату і знайти її за ID"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        expense_data = {
            "amount": 250.50,
            "category_id": 2,
            "description": "Інтеграційний тест",
            "expense_date": str(date.today())
        }
        
        # Act — зберігаємо
        expense_id = repo.save(expense_data)
        
        # Act — знаходимо
        found_expense = repo.find_by_id(expense_id)
        
        # Assert
        assert found_expense is not None
        assert found_expense["id"] == expense_id
        assert found_expense["amount"] == 250.50
        assert found_expense["category_id"] == 2
        assert found_expense["description"] == "Інтеграційний тест"

    @pytest.mark.integration
    def test_update_changes_expense_data(self, in_memory_db):
        """Оновлення витрати змінює дані в БД"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        original_data = {
            "amount": 100.0,
            "category_id": 1,
            "description": "Оригінальний опис",
            "expense_date": str(date.today())
        }
        expense_id = repo.save(original_data)
        
        # Act — оновлюємо
        updated_data = {
            "amount": 200.0,
            "category_id": 3,
            "description": "Оновлений опис",
            "expense_date": str(date.today())
        }
        result = repo.update(expense_id, updated_data)
        
        # Assert — перевіряємо що оновлення успішне
        assert result is True
        
        # Assert — перевіряємо що дані змінились
        updated_expense = repo.find_by_id(expense_id)
        assert updated_expense["amount"] == 200.0
        assert updated_expense["category_id"] == 3
        assert updated_expense["description"] == "Оновлений опис"

    @pytest.mark.integration
    def test_delete_removes_expense(self, in_memory_db):
        """Видалення витрати прибирає її з БД"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        expense_data = {
            "amount": 150.0,
            "category_id": 2,
            "description": "Для видалення",
            "expense_date": str(date.today())
        }
        expense_id = repo.save(expense_data)
        
        # Act — видаляємо
        result = repo.delete(expense_id)
        
        # Assert — перевіряємо що видалення успішне
        assert result is True
        
        # Assert — перевіряємо що витрати більше немає
        deleted_expense = repo.find_by_id(expense_id)
        assert deleted_expense is None

    @pytest.mark.integration
    def test_find_nonexistent_expense_returns_none(self, in_memory_db):
        """Пошук неіснуючої витрати повертає None"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        nonexistent_id = 99999
        
        # Act
        result = repo.find_by_id(nonexistent_id)
        
        # Assert
        assert result is None

    @pytest.mark.integration
    def test_update_nonexistent_expense_returns_false(self, in_memory_db):
        """Оновлення неіснуючої витрати повертає False"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        nonexistent_id = 99999
        update_data = {
            "amount": 100.0,
            "category_id": 1,
            "description": "Тест",
            "expense_date": str(date.today())
        }
        
        # Act
        result = repo.update(nonexistent_id, update_data)
        
        # Assert
        assert result is False

    @pytest.mark.integration
    def test_delete_nonexistent_expense_returns_false(self, in_memory_db):
        """Видалення неіснуючої витрати повертає False"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        nonexistent_id = 99999
        
        # Act
        result = repo.delete(nonexistent_id)
        
        # Assert
        assert result is False

    @pytest.mark.integration
    def test_multiple_expenses_saved_independently(self, in_memory_db):
        """Кілька витрат зберігаються незалежно"""
        # Arrange
        repo = ExpenseRepository(in_memory_db)
        
        # Act — зберігаємо 3 витрати
        id1 = repo.save({
            "amount": 100.0,
            "category_id": 1,
            "description": "Перша",
            "expense_date": str(date.today())
        })
        id2 = repo.save({
            "amount": 200.0,
            "category_id": 2,
            "description": "Друга",
            "expense_date": str(date.today())
        })
        id3 = repo.save({
            "amount": 300.0,
            "category_id": 3,
            "description": "Третя",
            "expense_date": str(date.today())
        })
        
        # Assert — всі ID різні
        assert id1 != id2 != id3
        
        # Assert — всі витрати можна знайти
        assert repo.find_by_id(id1)["amount"] == 100.0
        assert repo.find_by_id(id2)["amount"] == 200.0
        assert repo.find_by_id(id3)["amount"] == 300.0
