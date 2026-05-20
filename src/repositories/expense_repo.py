"""
Репозиторій для роботи з витратами в базі даних
"""
import sqlite3
from typing import Optional, Dict, Any
from datetime import date


class ExpenseRepository:
    """Репозиторій для збереження та отримання витрат з БД"""

    def __init__(self, connection: sqlite3.Connection):
        """
        Ініціалізація репозиторію з підключенням до БД.
        
        Args:
            connection: SQLite з'єднання
        """
        self.conn = connection

    def save(self, expense: Dict[str, Any]) -> int:
        """
        Зберігає витрату в БД.
        
        Args:
            expense: Словник з даними витрати (amount, category_id, description, expense_date)
        
        Returns:
            int: ID збереженої витрати
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (amount, category_id, description, expense_date)
            VALUES (?, ?, ?, ?)
        """, (
            expense["amount"],
            expense["category_id"],
            expense["description"],
            expense["expense_date"]
        ))
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, expense_id: int) -> Optional[Dict[str, Any]]:
        """
        Знаходить витрату за ID.
        
        Args:
            expense_id: ID витрати
        
        Returns:
            Dict з даними витрати або None якщо не знайдено
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, amount, category_id, description, expense_date
            FROM expenses
            WHERE id = ?
        """, (expense_id,))
        
        row = cursor.fetchone()
        if row is None:
            return None
        
        return {
            "id": row[0],
            "amount": row[1],
            "category_id": row[2],
            "description": row[3],
            "expense_date": row[4]
        }

    def update(self, expense_id: int, data: Dict[str, Any]) -> bool:
        """
        Оновлює дані витрати.
        
        Args:
            expense_id: ID витрати
            data: Нові дані для оновлення
        
        Returns:
            bool: True якщо оновлено, False якщо витрату не знайдено
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE expenses
            SET amount = ?, category_id = ?, description = ?, expense_date = ?
            WHERE id = ?
        """, (
            data.get("amount"),
            data.get("category_id"),
            data.get("description"),
            data.get("expense_date"),
            expense_id
        ))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, expense_id: int) -> bool:
        """
        Видаляє витрату з БД.
        
        Args:
            expense_id: ID витрати
        
        Returns:
            bool: True якщо видалено, False якщо витрату не знайдено
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
        return cursor.rowcount > 0
