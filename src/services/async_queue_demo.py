# src/services/async_queue_demo.py
import asyncio
import time
import random

async def producer(queue: asyncio.Queue, n: int):
    """Генерує n задач і додає їх у чергу"""
    for i in range(1, n + 1):
        # Імітація генерації задачі
        await asyncio.sleep(0.1)
        item = f"Задача #{i}"
        await queue.put(item)
        print(f"[Producer] Додано в чергу: {item}")

async def consumer(name: str, queue: asyncio.Queue):
    """Обробляє задачі з черги"""
    while True:
        # Отримуємо задачу з черги
        item = await queue.get()
        try:
            print(f"  [Consumer {name}] Почав обробку: {item}")
            # Імітація обробки задачі (0.2 сек за умовою)
            await asyncio.sleep(0.2)
            print(f"  [Consumer {name}] ЗАВЕРШИВ: {item}")
        finally:
            # Позначаємо задачу як виконану
            queue.task_done()

async def run_queue_demo():
    print("--- ПР-12.2: Producer-Consumer (Async Queue) ---")
    queue = asyncio.Queue()
    num_tasks = 10
    num_consumers = 3

    start_time = time.perf_counter()

    # 1. Запускаємо Producer
    producer_task = asyncio.create_task(producer(queue, num_tasks))

    # 2. Запускаємо Consumer-ів
    consumers = [
        asyncio.create_task(consumer(f"C{i+1}", queue))
        for i in range(num_consumers)
    ]

    # 3. Чекаємо, поки Producer закінчить додавати задачі
    await producer_task

    # 4. Чекаємо, поки черга стане порожньою (всі задачі оброблені)
    await queue.join()

    # 5. Зупиняємо Consumer-ів (вони працюють у нескінченному циклі)
    for c in consumers:
        c.cancel()

    end_time = time.perf_counter()
    total_parallel_time = end_time - start_time

    # Розрахунок послідовного часу для порівняння:
    # 10 * 0.1 (генерація) + 10 * 0.2 (обробка) = 1.0 + 2.0 = 3.0 сек
    sequential_time = (num_tasks * 0.1) + (num_tasks * 0.2)

    print("-" * 40)
    print(f"Кількість задач: {num_tasks}")
    print(f"Кількість воркерів: {num_consumers}")
    print(f"Загальний час (Паралельно): {total_parallel_time:.3f} сек")
    print(f"Очікуваний час (Послідовно): ~{sequential_time:.3f} сек")
    print(f"Ефективність: ~{sequential_time / total_parallel_time:.1f}x швидше")
    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run_queue_demo())
