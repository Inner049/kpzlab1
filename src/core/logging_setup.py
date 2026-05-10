# src/core/logging_setup.py
import logging
import json
import os
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Кастомний форматер для PRODUCTION режиму"""
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)

def setup_logging():
    # Можемо змінювати ENV на 'production' для JSON-логів
    env = os.getenv("ENV", "development").lower()
    logger = logging.getLogger()
    
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler()

    if env == "production":
        logger.setLevel(logging.WARNING)
        handler.setFormatter(JSONFormatter())
    else:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)

    logger.addHandler(handler)
    logging.info("Логування налаштовано. Режим: %s", env)
