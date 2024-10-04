import os
from pathlib import Path

from osm2you.settings import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGGING_FILE_PATH = os.path.join(BASE_DIR, "log/pytest.log")
LOGGING_LOGGERS = {
    "django": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "osm2you": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGGING_FILE_PATH,
            "formatter": "verbose",
        },
    },
    "loggers": LOGGING_LOGGERS,
}


USE_TZ = False
