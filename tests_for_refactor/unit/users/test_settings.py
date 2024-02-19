from django.conf import settings


class TestUsersSettings:
    def test_installedapps_settings(self):
        assert (
            "users" in settings.INSTALLED_APPS
        ), "Check that users includet to INSTALLED_APPS"

    def test_auth_user_model_settings(self):
        assert (
            settings.AUTH_USER_MODEL == "users.User"
        ), "Check AUTH_USER_MODEL settings"
