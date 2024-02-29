import os
from datetime import timedelta
from pathlib import Path

import dotenv
from celery.schedules import crontab
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# DJANGO
DEBUG = os.getenv("ST_DEBUG", "False") == "True"
DEBUG_SQL = os.getenv("ST_DEBUG_SQL", "False") == "True"

SECRET_KEY = os.getenv("ST_SECRET_KEY")

CSRF_TRUSTED_ORIGINS = ["http://localhost", "https://osm.w2c.net.eu.org"]
CORS_ORIGIN_WHITELIST = ["http://localhost"]
if DEBUG:
    CSRF_TRUSTED_ORIGINS.append("http://localhost:3000")
    CORS_ORIGIN_WHITELIST.append("http://localhost:3000")
CORS_ALLOW_HEADERS = list(default_headers) + ["access-control-allow-origin"]
ALLOWED_HOSTS = os.getenv("ST_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django.contrib.gis",
    "rest_framework",
    "rest_framework_gis",
    "djoser",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "django_celery_beat",
    "core",
    "api",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "osm2you.urls"

WSGI_APPLICATION = "osm2you.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "TEST": {
            "NAME": os.getenv("DB_TEST_NAME"),
        },
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

DJOSER = {
    "SERIALIZERS": {
        "user_create": "api.serializers.users.CustomUserCreateSerializer",
        "user": "api.serializers.users.CustomUserFullSerializer",
        "current_user": "api.serializers.users.CustomUserFullSerializer",
    },
    "PERMISSIONS": {
        "activation": ["api.permissions.DenyAll"],
        "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
        "username_reset": ["api.permissions.DenyAll"],
        "username_reset_confirm": ["api.permissions.DenyAll"],
        "set_username": ["api.permissions.DenyAll"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user_delete": ["api.permissions.DenyAll"],
        "user": ["api.permissions.CurrentUserGetPut"],
        "user_list": ["api.permissions.DenyAll"],
        "token_create": ["rest_framework.permissions.AllowAny"],
        "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
    },
    "HIDE_USERS": True,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

# LOGGING
LOGGING_FILE_PATH = os.path.join(BASE_DIR, "log/django.log")
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
if DEBUG_SQL is True:
    LOGGING_LOGGERS["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
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

# CORE APP
MARKERS_RELATED_IN_RADIUS = 5000

OVERPASS = {
    "url": "https://overpass-api.de/api/interpreter",
    "main": {
        "wrap": """({subqueries});out;""",
        "subquery": """node["{tag_name}"="{tag_value}"]({south},{west},{north},{east});""",
    },
    "related": {
        "wrap": """({subqueries});out center;""",
        "subquery": """node["{tag_name}"="{tag_value}"](around:{radius},{lat},{lon});""",
    },
    "related_batch": {
        "wrap": """({subqueries});out center;""",
        "subquery": """node(around:{radius},{lat},{lon})[{tags}];""",
        "square_size": 8,
        "packege_size": 30,
    },
}

CLUSTERING = {
    "square_size": [
        1,
        4,
        8,
        12,
        24,
    ]
}
CLUSTERING_DENCITY = 12

if CLUSTERING["square_size"] != sorted(CLUSTERING["square_size"]):
    raise ValueError("CLUSTERING['square_size'] must be in ascending order.")


# CELERY
CELERY_BROKER_URL = (
    f"{os.getenv('REDIS_USER')}://{os.getenv('REDIS_HOST')}:"
    f"{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_INDEX')}"
)
CELERY_RESULT_BACKEND = (
    f"{os.getenv('REDIS_USER')}://{os.getenv('REDIS_HOST')}:"
    f"{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_INDEX')}"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "run_scrap_markers_main": {
        # Run every night at 2 AM
        "task": "markers.tasks.run_scrap_markers_main",
        "schedule": crontab(minute=0, hour=2),
    },
}
