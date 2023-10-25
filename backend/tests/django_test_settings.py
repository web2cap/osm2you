from mymap.settings import *

LOGGING_FILE_PATH = "log/test_django.log"
LOGGING_LOGGERS = {
    "django": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "mymap": {
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
