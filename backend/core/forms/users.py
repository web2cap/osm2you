from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core.models.users import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "bio",
            "instagram",
            "telegram",
            "facebook",
        )
