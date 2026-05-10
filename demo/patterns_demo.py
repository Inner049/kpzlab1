# demo/patterns_demo.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 50)
print("ПАТЕРНИ ПРОЕКТУВАННЯ — ДЕМОНСТРАЦІЯ")
print("=" * 50)

# 1. Singleton
print("\n--- 1. Singleton: AppConfig ---")
from src.core.config import get_config
cfg1 = get_config()
cfg2 = get_config()
print(f"cfg1 is cfg2: {cfg1 is cfg2}")

# 2. Factory Method
print("\n--- 2. Factory Method: ReportFactory ---")
from src.patterns.report_factory import ReportFactory, ReportGenerator

# Демонстрація Завдання 8.2 (Розширення фабрики)
class ExcelReportGenerator(ReportGenerator):
    def generate(self, data: list) -> str:
        return f"Згенеровано EXCEL звіт для {len(data)} записів."

ReportFactory.register("excel", ExcelReportGenerator)

test_data = [1, 2, 3]
for fmt in ["csv", "pdf", "json", "excel"]:
    report_gen = ReportFactory.create(fmt)
    print(f"Формат {fmt.upper()}: {report_gen.generate(test_data)}")

# 3. Builder
print("\n--- 3. Builder: ExpenseBuilder ---")
from src.patterns.expense_builder import ExpenseBuilder
from datetime import date, timedelta

expense = (ExpenseBuilder()
           .amount(1450.50)
           .category(2)
           .date(date.today() - timedelta(days=1))
           .description("Закупівля продуктів на тиждень")
           .tag("їжа")
           .tag("супермаркет")
           .build())
print(expense)
print("=" * 50)

print("\n" + "=" * 50)
print("ПР-9: ПОВЕДІНКОВІ ТА СТРУКТУРНІ ПАТЕРНИ")
print("=" * 50)

# 1. OBSERVER
print("\n--- 1. Observer (EventBus) ---")
from src.patterns.event_bus import EventBus, log_expense, check_budget, send_alert
bus = EventBus()
bus.on("expense.added", log_expense)
bus.on("expense.added", check_budget)
bus.on("expense.added", send_alert)

# 2. STRATEGY + FACTORY
print("\n--- 2. Strategy + Factory ---")
from src.patterns.expense_strategy import StrategyFactory, ExpenseReportContext
expenses_data = [
    {"amount": 500, "category": "Їжа"},
    {"amount": 1200, "category": "Техніка"},
    {"amount": 100, "category": "Їжа"}
]

for strategy_name in ["total", "category", "average"]:
    strategy = StrategyFactory.create(strategy_name)
    context = ExpenseReportContext(strategy)
    print(f"Стратегія '{strategy_name}': {context.generate(expenses_data)}")

# 3. DECORATOR
print("\n--- 3. Decorator (@cache) ---")
from src.core.decorators import cache

@cache
def expensive_calculation(x):
    return x * x

expensive_calculation(5) # Обчислить
expensive_calculation(5) # Візьме з кешу

# 4. FACADE
print("\n--- 4. Facade ---")
from src.patterns.expense_facade import ExpenseFacade
facade = ExpenseFacade()
# Цей виклик запустить Decorator (Timer) і Observer (EventBus)
facade.process_new_expense(1500, "Техніка")