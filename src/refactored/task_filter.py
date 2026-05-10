# src/refactored/task_filter.py
import sqlite3
import logging
from enum import Enum
from typing import List, Dict

logger = logging.getLogger(__name__)

# Замінюємо магічні числа на Enum та константи
class TaskStatus(Enum):
    ACTIVE = 1
    PENDING = 2

MIN_PRIORITY_FOR_PENDING = 5
DISCOUNT_RATE = 0.85
NO_DISCOUNT_RATE = 0.95
DISCOUNT_THRESHOLD = 500

def _filter_valid_tasks(tasks: List[Dict]) -> List[Dict]:
    """Виділена підфункція для фільтрації задач (Extract Function)"""
    valid_tasks = []
    for task in tasks:
        if task is None:
            continue
            
        status = task.get('status')
        if status == TaskStatus.ACTIVE.value:
            valid_tasks.append(task)
        elif status == TaskStatus.PENDING.value and task.get('priority', 0) > MIN_PRIORITY_FOR_PENDING:
            valid_tasks.append(task)
            
    return valid_tasks

def apply_discounts(tasks: List[Dict], has_discount: bool) -> List[Dict]:
    """Головна функція з чіткою назвою та обробкою помилок"""
    filtered_tasks = _filter_valid_tasks(tasks)
    
    for task in filtered_tasks:
        price = task.get('price', 0)
        if has_discount:
            task['price'] = price * DISCOUNT_RATE
        elif price > DISCOUNT_THRESHOLD:
            task['price'] = price * NO_DISCOUNT_RATE

    try:
        # Безпечна робота з файлами через менеджер контексту
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(str(filtered_tasks) + "\n")
    except IOError as e:
        logger.error("Помилка запису в лог: %s", e)
        
    return filtered_tasks

class TaskManager:
    """Виправлений клас для роботи з БД (усунуто SQL Injection)"""
    def __init__(self, db_path: str = 'tasks.db'):
        self.db = sqlite3.connect(db_path)

    def update_task(self, task_id: int, name: str) -> bool:
        cursor = self.db.cursor()
        
        # Безпечний параметризований запит
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if cursor.fetchone() is not None:
            cursor.execute("UPDATE tasks SET name = ? WHERE id = ?", (name, task_id))
            cursor.execute("INSERT INTO logs (task_id, name, action) VALUES (?, ?, ?)", 
                           (task_id, name, "updated"))
            self.db.commit()
            return True
        return False
