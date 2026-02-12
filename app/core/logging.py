import asyncio
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True
):
    """Настройка логирования для всего приложения"""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
   
    root_logger.handlers.clear()
    

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        root_logger.addHandler(console_handler)
    

    if log_to_file:
        file_handler = RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root_logger.addHandler(file_handler)
        

        error_handler = RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)
    
 
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Логирование настроено")
    
    return root_logger

class RequestIdFilter(logging.Filter):
    """Добавляет request_id в каждый лог"""
    
    def __init__(self):
        self.request_id = None
    
    def set_request_id(self, request_id: str):
        self.request_id = request_id
    
    def filter(self, record):
        record.request_id = self.request_id or "-"
        return True


def log_function_call(func):
    """Декоратор для логирования вызовов функций"""
    
    async def async_wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Вызов {func.__name__} с args={args}, kwargs={kwargs}")
        
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Результат {func.__name__}: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}", exc_info=True)
            raise
    
    def sync_wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Вызов {func.__name__} с args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Результат {func.__name__}: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}", exc_info=True)
            raise
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper