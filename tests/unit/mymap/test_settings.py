import logging

from django.conf import settings


class TestMymapSettings:
    def test_debug_settings(self):
        """Test that DEBUG is false."""

        assert not settings.DEBUG, "Check that DEBUG is disabled in Django settings"

    def test_database_settings(self):
        """Test db adapter is setted correct."""
        assert (
            settings.DATABASES["default"]["ENGINE"]
            == "django.contrib.gis.db.backends.postgis"
        ), "Check you are using postgresql database"

    def test_logging_settings(self):
        """Test that django logger with level INFO or low exist.
        Test that file handler setted. Test that console handler setted."""

        django_logger = logging.getLogger("django")

        assert django_logger.level in (
            logging.DEBUG,
            logging.INFO,
        ), "Check django logging leavel"

        handlers = django_logger.handlers
        assert logging.FileHandler in [
            type(handler) for handler in django_logger.handlers
        ], "Check that django file handler setted up"

        file_handler = next(
            handler for handler in handlers if isinstance(handler, logging.FileHandler)
        )
        assert isinstance(file_handler, logging.FileHandler)
        assert file_handler.level in (
            logging.DEBUG,
            logging.INFO,
        ), "Check django file handler logging leavel"
        assert (
            file_handler.formatter._fmt == "{levelname} {asctime} {module} {message}"
        ), "Chech format of the 'file' handler"
        assert (
            file_handler.baseFilename
        ), "Chech that filename of the file handler filled"

        assert (
            len(file_handler.baseFilename) > 4
            and file_handler.baseFilename[-4:] == ".log"
        ), "Chech filenamefile handler filenamefile format"

        console_handler = next(
            handler
            for handler in handlers
            if isinstance(handler, logging.StreamHandler)
        )
        assert isinstance(
            console_handler, logging.StreamHandler
        ), "Check format of the 'console' handler."
        assert console_handler.level in (
            logging.DEBUG,
            logging.INFO,
        ), "Check django console handler logging leavel"
        assert (
            console_handler.formatter._fmt == "{levelname} {asctime} {module} {message}"
        ), "Chech format of the console handler"

    def test_csrf_settings(self):
        """Check that CSRF settings filled in."""

        assert len(
            settings.CSRF_TRUSTED_ORIGINS
        ), "Check that CSRF_TRUSTED_ORIGINS filled in"

    def test_cors_settings(self):
        """Check that CORS settings filled in."""

        assert (
            "corsheaders" in settings.INSTALLED_APPS
        ), "Check that corsheaders includet to INSTALLED_APPS"
        assert (
            not hasattr(settings, "CORS_ALLOW_ALL_ORIGINS")
            or not settings.CORS_ALLOW_ALL_ORIGINS
        ), "Check that CORS_ALLOW_ALL_ORIGINS disabled"
        assert (
            "access-control-allow-origin" in settings.CORS_ALLOW_HEADERS
        ), "Check access-control-allow-origin is present in CORS_ALLOW_HEADERS"

        assert len(
            settings.CORS_ORIGIN_WHITELIST
        ), "Check that CORS_ORIGIN_WHITELIST filled in"

    def test_allowed_host_settings(self):
        """Check that ALLOWED_HOSTS and IP settings filled in."""

        assert len(settings.ALLOWED_HOSTS), "Check that CSRF_TRUSTED_ORIGINS filled in"
        assert (
            "127.0.0.1" in settings.INTERNAL_IPS
        ), "Check that 127.0.0.1 filled in INTERNAL_IPS"

    def test_email_backend_settings(self):
        assert hasattr(
            settings, "EMAIL_BACKEND"
        ), """Check that EMAIL_BACKEND settings filled in."""

    def test_static_media_settings(self):
        assert hasattr(settings, "STATIC_URL") and len(
            settings.STATIC_URL
        ), """Check that STATIC_URL settings filled."""

        assert hasattr(settings, "MEDIA_URL") and len(
            settings.MEDIA_URL
        ), """Check that MEDIA_URL settings filled."""

    def test_swagger_settings(self):
        assert hasattr(
            settings, "SWAGGER_SETTINGS"
        ), """Check that STATIC_URL settings filled."""

        assert (
            "drf_yasg" in settings.INSTALLED_APPS
        ), "Check that drf_yasg includet to INSTALLED_APPS"
