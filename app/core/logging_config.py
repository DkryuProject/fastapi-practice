import logging
from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            },
            "detail": {
                "format": (
                    "[%(asctime)s] [%(levelname)s] [%(name)s] "
                    "[%(filename)s:%(lineno)d] %(message)s"
                )
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
            },

            "file_info": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "detail",
                "filename": "logs/info.log",
                "when": "midnight",
                "backupCount": 7,
                "encoding": "utf-8",
                "level": "INFO",
            },

            "file_error": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "detail",
                "filename": "logs/error.log",
                "when": "midnight",
                "backupCount": 7,
                "encoding": "utf-8",
                "level": "ERROR",
            },
        },

        "loggers": {
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            },
            "app": {
                "handlers": ["console", "file_info", "file_error"],
                "level": "DEBUG",
                "propagate": False
            },
        }
    })

    logging.getLogger("app").info("Logging initialized")
