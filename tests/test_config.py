# tests/test_config.py
from src.core.config import AppConfig, get_config

def test_singleton_same_instance():
    cfg1 = AppConfig()
    cfg2 = AppConfig()
    assert cfg1 is cfg2, "Singleton: cfg1 і cfg2 мають бути одним об'єктом"
    print("Test 1 Passed: cfg1 is cfg2")

def test_config_loads_once():
    cfg = get_config()
    assert hasattr(cfg, 'DEBUG')
    assert hasattr(cfg, 'DB_URL')
    print("Config:", cfg)
    print("Test 2 Passed: Config loads correctly")

if __name__ == "__main__":
    test_singleton_same_instance()
    test_config_loads_once()
    print("Усі перевірки пройдено!")