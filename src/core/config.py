# src/core/config.py
import os
import threading

class AppConfig:
    """
    Thread-safe Singleton — єдиний об'єкт конфігурації застосунку.
    """
    _instance = None
    _lock = threading.Lock() # Блокування для безпеки в багатопотоковому середовищі

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._loaded = False
        return cls._instance

    def load(self):
        """Завантажити конфігурацію (тільки один раз)"""
        if self._loaded:
            return
        
        self.DEBUG       = os.getenv("DEBUG", "false").lower() == "true"
        self.DB_URL      = os.getenv("DB_URL", "postgresql://user:pass@localhost/expense_db")
        self.SECRET_KEY  = os.getenv("SECRET_KEY", "dev-secret-key")
        self.LOG_LEVEL   = os.getenv("LOG_LEVEL", "INFO")
        self._loaded     = True
        print(f"[Config] Завантажено: DEBUG={self.DEBUG}, DB={self.DB_URL}")

    def __repr__(self):
        return f"AppConfig(debug={self.DEBUG}, db={self.DB_URL})"

def get_config() -> AppConfig:
    cfg = AppConfig()
    cfg.load()
    return cfg

# ЗАВДАННЯ ДЛЯ ЗАКРІПЛЕННЯ 8.1 B:
# Наведений у завданні код НЕ є Singleton, оскільки він не обмежує створення нових екземплярів класу. 
# Кожен виклик Config() створює новий об'єкт у пам'яті (тому c1 is c2 повертає False). 
# Використання спільної змінної класу (data) робить стан об'єктів спільним, але це патерн Monostate (Borg), 
# а не Singleton. Справжній Singleton гарантує існування лише одного екземпляра класу.