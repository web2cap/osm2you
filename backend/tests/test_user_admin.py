import pytest
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.admin import CustomUserAdmin
from users.models import User


# @pytest.mark.django_db
class TestCustomUserAdmin:
    def test_user_registration_in_admin(self):
        assert (
            User in admin.site._registry
        ), "User model should be registered in admin site"
        admin_class = admin.site._registry[User]
        assert isinstance(
            admin_class, CustomUserAdmin
        ), "User model should be registered with CustomUserAdmin"

    def test_custom_user_admin_inherits_from_user_admin(self):
        assert issubclass(
            CustomUserAdmin, UserAdmin
        ), "CustomUserAdmin should inherit from UserAdmin"

    def test_custom_user_admin_attributes(self):
        custom_admin = CustomUserAdmin(User, admin.site)
        assert custom_admin.add_form == CustomUserAdmin.add_form
        assert custom_admin.form == CustomUserAdmin.form
        assert custom_admin.model == User

    def test_custom_user_admin_list_display(self):
        custom_admin = CustomUserAdmin(User, admin.site)
        expected_list_display = (
            "email",
            "username",
            "is_staff",
            "is_active",
        )
        assert custom_admin.list_display == expected_list_display
