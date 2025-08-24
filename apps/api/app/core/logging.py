"""
Logging configuration for Homlo API
"""

import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any

from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Logging configuration
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(timestamp)s %(level)s %(name)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "formatter": "detailed" if settings.DEBUG else "default",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json" if settings.LOG_FORMAT == "json" else "default",
                "filename": log_dir / "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "json" if settings.LOG_FORMAT == "json" else "detailed",
                "filename": log_dir / "error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json" if settings.LOG_FORMAT == "json" else "default",
                "filename": log_dir / "access.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file", "error_file"],
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "propagate": False,
            },
            "app": {  # Application logger
                "handlers": ["console", "file", "error_file"],
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "propagate": False,
            },
            "uvicorn": {  # Uvicorn logger
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {  # Access logs
                "handlers": ["access_file"],
                "level": "INFO",
                "propagate": False,
            },
            "sqlalchemy": {  # SQLAlchemy logger
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": False,
            },
            "celery": {  # Celery logger
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "redis": {  # Redis logger
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": False,
            },
            "httpx": {  # HTTP client logger
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }
    
    # Apply logging configuration
    logging.config.dictConfig(log_config)
    
    # Get main application logger
    logger = logging.getLogger("app")
    
    # Set log level based on environment
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # Log startup message
    logger.info(f"Logging configured for {settings.ENVIRONMENT} environment")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    logger.info(f"Log format: {settings.LOG_FORMAT}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(f"app.{name}")


# Custom log formatter for structured logging
class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with additional context"""
        # Add extra fields to record
        if not hasattr(record, 'timestamp'):
            record.timestamp = self.formatTime(record)
        
        if not hasattr(record, 'level'):
            record.level = record.levelname
        
        if not hasattr(record, 'logger'):
            record.logger = record.name
        
        # Format message
        message = super().format(record)
        
        # Add extra context if available
        if hasattr(record, 'extra_data'):
            message += f" | Extra: {record.extra_data}"
        
        return message


# Context manager for logging context
class LogContext:
    """Context manager for adding context to logs"""
    
    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
        self.old_context = {}
    
    def __enter__(self):
        # Store old context
        for key, value in self.context.items():
            if hasattr(self.logger, key):
                self.old_context[key] = getattr(self.logger, key)
            setattr(self.logger, key, value)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore old context
        for key, value in self.old_context.items():
            setattr(self.logger, key, value)
        for key in self.context:
            if key not in self.old_context:
                delattr(self.logger, key)


# Logging decorator
def log_function_call(logger: logging.Logger = None):
    """Decorator to log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if logger is None:
                func_logger = get_logger(func.__module__)
            else:
                func_logger = logger
            
            func_logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                func_logger.debug(f"{func.__name__} returned {result}")
                return result
            except Exception as e:
                func_logger.error(f"{func.__name__} failed with error: {e}", exc_info=True)
                raise
        return wrapper
    return decorator


# Performance logging
def log_performance(logger: logging.Logger = None):
    """Decorator to log function performance"""
    import time
    import functools
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if logger is None:
                func_logger = get_logger(func.__module__)
            else:
                func_logger = logger
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                func_logger.info(f"{func.__name__} completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                func_logger.error(f"{func.__name__} failed after {duration:.3f}s with error: {e}", exc_info=True)
                raise
        return wrapper
    return decorator
