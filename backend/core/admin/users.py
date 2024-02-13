from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms.users import CustomUserChangeForm, CustomUserCreationForm
from core.models.users import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "email",
        "username",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            "Main",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                )
            },
        ),
        (
            "Social",
            {
                "fields": (
                    "bio",
                    "instagram",
                    "telegram",
                    "facebook",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "bio",
        "instagram",
        "telegram",
        "facebook",
    )
    ordering = ("email",)
