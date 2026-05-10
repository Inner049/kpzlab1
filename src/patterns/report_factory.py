# src/patterns/report_factory.py
from abc import ABC, abstractmethod

# 1. Абстрактний продукт
class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: list) -> str:
        pass

# 2. Конкретні продукти (МІНІМУМ 3)
class CSVReportGenerator(ReportGenerator):
    def generate(self, data: list) -> str:
        return f"Згенеровано CSV звіт для {len(data)} записів."

class PDFReportGenerator(ReportGenerator):
    def generate(self, data: list) -> str:
        return f"Згенеровано PDF звіт для {len(data)} записів."

class JSONReportGenerator(ReportGenerator):
    def generate(self, data: list) -> str:
        return f"Згенеровано JSON звіт для {len(data)} записів."

# 3. Фабрика з динамічним реєстром (OCP)
class ReportFactory:
    _registry: dict = {
        "csv": CSVReportGenerator,
        "pdf": PDFReportGenerator,
        "json": JSONReportGenerator,
    }

    @classmethod
    def create(cls, format_type: str) -> ReportGenerator:
        cls_ = cls._registry.get(format_type.lower())
        if cls_ is None:
            available = list(cls._registry.keys())
            raise ValueError(f"Невідомий формат '{format_type}'. Доступні: {available}")
        return cls_()

    @classmethod
    def register(cls, name: str, generator_cls):
        """Розширення без зміни фабрики (принцип OCP)"""
        cls._registry[name.lower()] = generator_cls