# src/patterns/expense_builder.py
from datetime import date
from typing import List, Optional

class ExpenseModel:
    def __init__(self):
        self.amount: float = 0.0
        self.category_id: int = 0
        self.date: date = date.today()
        self.description: Optional[str] = None
        self.tags: List[str] = []
        
    def __str__(self):
        return f"Expense: {self.amount} UAH | Date: {self.date} | Desc: {self.description} | Tags: {self.tags}"

class ExpenseBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._expense = ExpenseModel()
        return self

    def amount(self, val: float):
        if val <= 0:
            raise ValueError("Сума має бути більшою за нуль")
        self._expense.amount = val
        return self

    def category(self, cat_id: int):
        self._expense.category_id = cat_id
        return self

    def date(self, d: date):
        self._expense.date = d
        return self

    def description(self, desc: str):
        self._expense.description = desc
        return self

    def tag(self, t: str):
        if t not in self._expense.tags:
            self._expense.tags.append(t.lower())
        return self

    def build(self) -> ExpenseModel:
        return self._expense