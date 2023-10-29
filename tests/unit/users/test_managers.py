import pytest

from users.models import User


class TestUsersManagers:
    @pytest.mark.django_db
    def test_create_user(self, sample_console_user, sample_user_data):
        user = sample_console_user
        assert isinstance(user, User)
        assert user.email == sample_user_data["email"]
        assert user.check_password(sample_user_data["password"])

    def test_create_user_invalid_email(self, custom_user_manager, sample_user_data):
        with pytest.raises(ValueError):
            custom_user_manager.create_user("", sample_user_data["password"])

    @pytest.mark.django_db
    def test_create_superuser(self, sample_console_superuser, sample_user_data):
        user = sample_console_superuser
        assert isinstance(user, User)
        assert user.email == sample_user_data["email"]
        assert user.is_staff
        assert user.is_superuser

    @pytest.mark.django_db
    def test_create_superuser_non_staff(self, custom_user_manager, sample_user_data):
        with pytest.raises(ValueError):
            custom_user_manager.create_superuser(**sample_user_data, is_staff=False)

    def test_create_superuser_non_superuser(
        self, custom_user_manager, sample_user_data
    ):
        with pytest.raises(ValueError):
            custom_user_manager.create_superuser(
                **sample_user_data,
                is_superuser=False,
            )
