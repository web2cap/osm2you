from django.conf import settings


class TestUsersSettings:
    def test_auth_user_model_settings(self):
        assert settings.AUTH_USER_MODEL == "core.User", "Check AUTH_USER_MODEL settings"
