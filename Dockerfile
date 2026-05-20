# Stage 1: Builder - встановлення залежностей
FROM python:3.12-slim AS builder

# Встановлення системних залежностей для компіляції пакетів
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Створення робочої директорії
WORKDIR /app

# Копіювання файлу залежностей
COPY requirements.txt .

# Встановлення Python залежностей у user site-packages
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt


# Stage 2: Production - мінімальний образ
FROM python:3.12-slim AS production

# Встановлення тільки runtime залежностей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Створення non-root користувача для безпеки
RUN useradd -m -u 1000 appuser

# Встановлення робочої директорії
WORKDIR /app

# Копіювання встановлених пакетів з builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Копіювання коду застосунку
COPY --chown=appuser:appuser . .

# Додавання .local/bin до PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Перемикання на non-root користувача
USER appuser

# Відкриття порту
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Запуск застосунку
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
