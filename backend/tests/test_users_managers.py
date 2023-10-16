import pytest

from users.models import User


class TestUsersManagers:
    def test_create_user(self, db, sample_user):
        user = sample_user
        assert isinstance(user, User)
        assert user.email == "user@example.com"
        assert user.check_password("Password123")

    def test_create_user_invalid_email(self, custom_user_manager):
        with pytest.raises(ValueError):
            custom_user_manager.create_user("", "Password123")

    def test_create_superuser(self, db, sample_superuser):
        user = sample_superuser
        assert isinstance(user, User)
        assert user.email == "admin@example.com"
        assert user.is_staff
        assert user.is_superuser

    def test_create_superuser_non_staff(self, custom_user_manager):
        with pytest.raises(ValueError):
            custom_user_manager.create_superuser(
                "nonstaff@example.com", "Nonstaffpassword123", is_staff=False
            )

    def test_create_superuser_non_superuser(self, custom_user_manager):
        with pytest.raises(ValueError):
            custom_user_manager.create_superuser(
                "nonsuperuser@example.com",
                "Nonsuperpassword123",
                is_superuser=False,
            )
