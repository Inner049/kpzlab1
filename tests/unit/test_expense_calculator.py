"""
TDD: Тести для функції calculate_monthly_total
Написані ДО реалізації функції (Test-Driven Development)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from datetime import date
# Імпорт функції, якої ще немає — це нормально для TDD RED фази
from src.services.expense_calculator import calculate_monthly_total


class TestCalculateMonthlyTotal:
    """TDD тести для підрахунку місячної суми витрат"""

    @pytest.mark.tdd
    def test_calculate_monthly_total_returns_sum(self, sample_expenses_list):
        """Підраховує суму витрат за конкретний місяць"""
        # Arrange
        # sample_expenses_list містить:
        # - 100.0 (травень 2026)
        # - 200.0 (травень 2026)
        # - 50.0 (червень 2026) — не враховується
        # - 75.0 (травень 2026)
        
        # Act
        result = calculate_monthly_total(sample_expenses_list, month=5, year=2026)
        
        # Assert
        assert result == 375.0  # 100 + 200 + 75

    @pytest.mark.tdd
    def test_empty_list_returns_zero(self):
        """Порожній список витрат повертає 0"""
        # Act
        result = calculate_monthly_total([], month=5, year=2026)
        
        # Assert
        assert result == 0.0

    @pytest.mark.tdd
    def test_filters_other_months(self):
        """Фільтрує витрати з інших місяців"""
        # Arrange
        expenses = [
            {"amount": 100.0, "date": date(2026, 5, 1)},
            {"amount": 200.0, "date": date(2026, 6, 1)},  # інший місяць
            {"amount": 50.0, "date": date(2026, 5, 15)},
        ]
        
        # Act
        result = calculate_monthly_total(expenses, month=5, year=2026)
        
        # Assert
        assert result == 150.0  # лише травень

    @pytest.mark.tdd
    def test_filters_other_years(self):
        """Фільтрує витрати з інших років"""
        # Arrange
        expenses = [
            {"amount": 100.0, "date": date(2026, 5, 1)},
            {"amount": 200.0, "date": date(2025, 5, 1)},  # інший рік
            {"amount": 50.0, "date": date(2026, 5, 15)},
        ]
        
        # Act
        result = calculate_monthly_total(expenses, month=5, year=2026)
        
        # Assert
        assert result == 150.0  # лише 2026 рік

    @pytest.mark.tdd
    def test_invalid_month_raises_error(self):
        """Некоректний місяць (13) кидає ValueError"""
        # Arrange
        expenses = [{"amount": 100.0, "date": date(2026, 5, 1)}]
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            calculate_monthly_total(expenses, month=13, year=2026)
        
        assert "1 до 12" in str(exc_info.value)

    @pytest.mark.tdd
    def test_zero_month_raises_error(self):
        """Місяць 0 кидає ValueError"""
        expenses = [{"amount": 100.0, "date": date(2026, 5, 1)}]
        
        with pytest.raises(ValueError):
            calculate_monthly_total(expenses, month=0, year=2026)
