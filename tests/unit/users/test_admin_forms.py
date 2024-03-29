import pytest
from core.forms.users import CustomUserChangeForm, CustomUserCreationForm


class TestUsersAdminForms:
    @pytest.mark.django_db
    def test_custom_user_creation_form_valid(self, sample_admin_form_user_data):
        """If the CustomUserCreationForm is valid with valid form data."""

        form = CustomUserCreationForm(sample_admin_form_user_data)
        assert form.is_valid()

    @pytest.mark.django_db
    def test_custom_user_creation_form_invalid(self):
        """If the CustomUserCreationForm is invalid with empty form data."""

        form = CustomUserCreationForm(dict())
        assert not form.is_valid()

    @pytest.mark.django_db
    def test_custom_user_change_form_valid(self, admin_form_user_data_updated):
        """If the CustomUserChangeForm is valid with updatet form data."""

        form = CustomUserChangeForm(admin_form_user_data_updated)
        assert form.is_valid()

    @pytest.mark.django_db
    def test_custom_user_change_form_invalid(self):
        """If the CustomUserChangeForm is invalid with empty form data."""

        form = CustomUserChangeForm(dict())
        assert not form.is_valid()
