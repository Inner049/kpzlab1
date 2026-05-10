# src/patterns/expense_strategy.py
from abc import ABC, abstractmethod
from typing import List, Dict

# 1. Інтерфейс стратегії
class ReportStrategy(ABC):
    @abstractmethod
    def calculate(self, expenses: List[Dict]) -> str:
        pass

# 2. Конкретні стратегії (мінімум 3)
class TotalSumStrategy(ReportStrategy):
    def calculate(self, expenses: List[Dict]) -> str:
        total = sum(e.get("amount", 0) for e in expenses)
        return f"Загальна сума витрат: {total} UAH"

class CategorySumStrategy(ReportStrategy):
    def calculate(self, expenses: List[Dict]) -> str:
        categories = {}
        for e in expenses:
            cat = e.get("category", "Інше")
            categories[cat] = categories.get(cat, 0) + e.get("amount", 0)
        return f"По категоріям: {categories}"

class AverageExpenseStrategy(ReportStrategy):
    def calculate(self, expenses: List[Dict]) -> str:
        if not expenses:
            return "Немає витрат для обчислення середнього."
        avg = sum(e.get("amount", 0) for e in expenses) / len(expenses)
        return f"Середній чек: {avg:.2f} UAH"

# 3. Фабрика для стратегій (Завдання 9.2)
class StrategyFactory:
    _strategies = {
        "total": TotalSumStrategy,
        "category": CategorySumStrategy,
        "average": AverageExpenseStrategy
    }

    @classmethod
    def create(cls, strategy_name: str) -> ReportStrategy:
        strategy_class = cls._strategies.get(strategy_name.lower())
        if not strategy_class:
            raise ValueError(f"Стратегія {strategy_name} не знайдена.")
        return strategy_class()

# 4. Context
class ExpenseReportContext:
    def __init__(self, strategy: ReportStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ReportStrategy):
        self._strategy = strategy

    def generate(self, expenses: List[Dict]) -> str:
        return self._strategy.calculate(expenses)
