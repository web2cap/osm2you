import pytest
from django.db.utils import IntegrityError

from users.models import User


@pytest.mark.django_db
def test_create_user(sample_user_data):
    """Test creating a new user with valid data."""

    user = User.objects.create_user(**sample_user_data)
    assert user.email == sample_user_data["email"]
    assert user.check_password(sample_user_data["password"])
    assert not user.is_superuser
    assert not user.is_staff


@pytest.mark.django_db
def test_create_unique_email(sample_user_data):
    """Test creating a new user with not unique email."""

    User.objects.create_user(**sample_user_data)
    with pytest.raises(IntegrityError):
        User.objects.create_user(**sample_user_data)


@pytest.mark.django_db
def test_create_unique_username(
    sample_user_data_with_username, sample_user_data_not_unique_username
):
    """Test creating a new user with not unique username."""

    User.objects.create_user(**sample_user_data_with_username)
    with pytest.raises(IntegrityError):
        User.objects.create_user(**sample_user_data_not_unique_username)


@pytest.mark.django_db
def test_autogenerate_username_on_save_user(sample_user_data):
    """Test autogenerating username whet creating a new user
    with empty username."""

    user = User.objects.create(**sample_user_data)
    user.save()
    assert user.username, "After saving user, username is empty"
    assert "hunter" in user.username, "Wrong autogenerated username format"


@pytest.mark.django_db
def test_create_user_empty_email():
    """Test creating a user with an empty email address."""
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="Password123")


@pytest.mark.django_db
def test_create_superuser(sample_superuser_data):
    """Test creating a superuser with valid data."""
    user = User.objects.create_superuser(**sample_superuser_data)
    assert user.email == sample_superuser_data["email"]
    assert user.check_password(sample_superuser_data["password"])
    assert user.is_superuser
    assert user.is_staff


@pytest.mark.django_db
def test_create_superuser_non_staff(sample_superuser_data):
    """Test creating a superuser without staff permissions."""
    sample_superuser_data["is_staff"] = False
    with pytest.raises(ValueError):
        User.objects.create_superuser(**sample_superuser_data)


@pytest.mark.django_db
def test_create_superuser_non_superuser(sample_superuser_data):
    """Test creating a superuser without superuser permissions."""
    sample_superuser_data["is_superuser"] = False
    with pytest.raises(ValueError):
        User.objects.create_superuser(**sample_superuser_data)
