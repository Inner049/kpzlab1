# src/patterns/expense_facade.py
from src.core.decorators import timer, retry
from src.patterns.event_bus import EventBus

# Імітація сервісів (можна винести в окремі файли)
class DatabaseService:
    def save(self, data):
        print(f"[DB] Збережено в базу: {data}")

class NotificationService:
    def send_push(self, msg):
        print(f"[PUSH] Відправлено нотифікацію: {msg}")

class AnalyticsService:
    def track(self, event):
        print(f"[ANALYTICS] Зафіксовано подію: {event}")

# Сам ФАСАД
class ExpenseFacade:
    """
    Фасад приховує складність.
    Один метод викликає БД, Сповіщення, Аналітику + тригерить Observer.
    """
    def __init__(self):
        self.db = DatabaseService()
        self.notif = NotificationService()
        self.analytics = AnalyticsService()
        self.bus = EventBus()

    @timer # Застосовуємо декоратор
    @retry(times=2) # Застосовуємо декоратор
    def process_new_expense(self, amount: float, category: str):
        print("\n--- Facade: Початок обробки ---")
        expense_data = {"amount": amount, "category": category}
        
        # 1. Сервіс 1
        self.db.save(expense_data)
        # 2. Сервіс 2
        self.notif.send_push(f"Витрачено {amount} UAH")
        # 3. Сервіс 3
        self.analytics.track("expense_created")
        # 4. Trigger Observer
        self.bus.emit("expense.added", expense_data)
        
        print("--- Facade: Завершено ---\n")
        return True
