# main.py
"""
Expense Tracker API - FastAPI Application
Точка входу для застосунку обліку витрат
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import get_config

# Ініціалізація конфігурації
config = get_config()

# Створення FastAPI застосунку
app = FastAPI(
    title="Expense Tracker API",
    description="API для обліку витрат з аналітикою та звітами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware для доступу з фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У production замінити на конкретні домени
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Кореневий endpoint"""
    return {
        "message": "Expense Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint для моніторингу та Docker health checks
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "production" if not config.DEBUG else "development",
        "database": "connected"  # У майбутньому можна додати реальну перевірку БД
    }


@app.get("/info")
async def info():
    """Інформація про застосунок"""
    return {
        "name": "Expense Tracker API",
        "version": "1.0.0",
        "description": "Застосунок обліку витрат з аналітикою",
        "features": [
            "Облік витрат",
            "Категоризація",
            "Аналітика та звіти",
            "Управління бюджетами"
        ]
    }


# Підключення роутів (коли будуть реалізовані)
# from src.api.routes import expenses, users
# app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
# app.include_router(users.router, prefix="/api/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn
    
    # Запуск сервера
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
