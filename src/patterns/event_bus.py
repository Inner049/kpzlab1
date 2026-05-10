# src/patterns/event_bus.py
from typing import Callable, Dict, List, Any

class EventBus:
    """
    Observer pattern (реалізація через Event Emitter).
    Централізована шина подій (Singleton для зручності).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers: Dict[str, List[Callable]] = {}
        return cls._instance

    def on(self, event_name: str, handler: Callable):
        """Підписка на подію (subscribe)"""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        print(f"[EventBus] Підписано обробник {handler.__name__} на подію '{event_name}'")

    def emit(self, event_name: str, data: Any = None):
        """Сповіщення про подію (notify)"""
        if event_name in self._subscribers:
            for handler in self._subscribers[event_name]:
                handler(data)

# Створюємо конкретні обробники (Observers) для події 'expense.added'
def log_expense(data):
    print(f"[OBSERVER 1: Logger] Збережено витрату: {data}")

def check_budget(data):
    print(f"[OBSERVER 2: Budget] Аналіз бюджету для суми {data.get('amount', 0)}...")

def send_alert(data):
    if data.get('amount', 0) > 1000:
        print(f"[OBSERVER 3: Alert] Увага! Велика витрата: {data.get('amount')}")
