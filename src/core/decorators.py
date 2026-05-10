# src/core/decorators.py
import time
import functools

def timer(func):
    """Декоратор 1: Вимірює час виконання"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] Функція '{func.__name__}' виконувалась {elapsed:.4f} сек")
        return result
    return wrapper

def cache(func):
    """Декоратор 2: Кешування результату"""
    _cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
            print(f"[CACHE] Обчислено та збережено для '{func.__name__}'")
        else:
            print(f"[CACHE] Взято з кешу для '{func.__name__}'")
        return _cache[key]
    return wrapper

def retry(times=3):
    """Бонус-декоратор 3: Перезапуск при помилці"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Спроба {attempt}/{times} провалилась: {e}")
                    if attempt == times:
                        raise
        return wrapper
    return decorator
