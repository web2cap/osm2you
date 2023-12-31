import os
from datetime import timedelta
from pathlib import Path

import dotenv
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

SECRET_KEY = os.getenv(
    "ST_SECRET_KEY",
)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "https://osm.w2c.net.eu.org",
]


CORS_ALLOW_HEADERS = list(default_headers) + [
    "access-control-allow-origin",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

DEBUG = os.getenv("ST_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "osm.w2c.net.eu.org",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

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
    "users",
    "markers",
    "tags",
    "stories",
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

AUTH_USER_MODEL = "users.User"
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
        "user_create": "users.serializers.UserCreateCustomSerializer",
        "user": "users.serializers.UserCustomSerializer",
        "current_user": "users.serializers.UserCustomSerializer",
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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

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
if DEBUG is True:
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
