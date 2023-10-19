from datetime import timedelta

import pytest
from django.conf import settings


class TestAPISettings:
    @pytest.mark.parametrize(
        "app",
        [
            "users",
            "rest_framework",
            "djoser",
            "rest_framework_simplejwt",
            "rest_framework.authtoken",
            "api",
        ],
    )
    def test_installedapps_settings(self, app):
        """Check that apps for api sered in INSTALLED_APPS"""

        assert (
            app in settings.INSTALLED_APPS
        ), f"Check that {app} includet to INSTALLED_APPS"

    def test_auth_user_model_settings(self):
        """Check that AUTH_USER_MODEL seted."""

        assert (
            settings.AUTH_USER_MODEL == "users.User"
        ), "Check AUTH_USER_MODEL settings"

    def test_rest_framework_settings(self):
        """Check REST_FRAMEWORK settings."""

        assert hasattr(
            settings, "REST_FRAMEWORK"
        ), "Check that REST_FRAMEWORK present in settings"

        assert (
            "rest_framework.permissions.AllowAny"
            in settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
        ), "Check that DEFAULT_PERMISSION_CLASSES set to AllowAny"

    def test_djoser_settings_exist(self):
        """Check that DJOSER exists in settings."""

        assert hasattr(settings, "DJOSER"), "Check that DJOSER present in settings"

    @pytest.mark.parametrize(
        "setting, value",
        [
            (settings.DJOSER, "SERIALIZERS"),
            (
                settings.DJOSER["SERIALIZERS"]["user_create"],
                "users.serializers.UserCreateCustomSerializer",
            ),
            (
                settings.DJOSER["SERIALIZERS"]["user"],
                "users.serializers.UserCustomSerializer",
            ),
            (
                settings.DJOSER["SERIALIZERS"]["current_user"],
                "users.serializers.UserCustomSerializer",
            ),
            (settings.DJOSER, "PERMISSIONS"),
            (
                settings.DJOSER["PERMISSIONS"]["user_create"],
                "rest_framework.permissions.AllowAny",
            ),
            (
                settings.DJOSER["PERMISSIONS"]["user_delete"],
                "core.permissions.DenyAll",
            ),
            (
                settings.DJOSER["PERMISSIONS"]["user"],
                "core.permissions.CreateOrCurrentUser",
            ),
            (
                settings.DJOSER["PERMISSIONS"]["user_list"],
                "core.permissions.DenyAll",
            ),
            (
                settings.DJOSER["PERMISSIONS"]["token_create"],
                "rest_framework.permissions.AllowAny",
            ),
            (
                settings.DJOSER["PERMISSIONS"]["token_destroy"],
                "rest_framework.permissions.IsAuthenticated",
            ),
        ],
    )
    def test_djoser_settings(self, setting, value):
        """Check DJOSER settings."""

        assert value in setting, f"Check that {value} present in {setting}"

    def test_simple_jwt_settings(self):
        """Check SIMPLE_JWT settings"""

        assert hasattr(
            settings, "SIMPLE_JWT"
        ), "Check that SIMPLE_JWT present in settings"
        assert (
            "ACCESS_TOKEN_LIFETIME" in settings.SIMPLE_JWT
            and type(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]) == timedelta
            and settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds() > 0
        ), "Check that ACCESS_TOKEN_LIFETIME present in settings.SIMPLE_JWT and setted correct."
        assert (
            "AUTH_HEADER_TYPES" in settings.SIMPLE_JWT
            and "Bearer" in settings.SIMPLE_JWT["AUTH_HEADER_TYPES"]
        ), "Check that Bearer in settings.SIMPLE_JWT.AUTH_HEADER_TYPES present."
