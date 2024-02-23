from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers.users import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, null=False
    )

    bio = models.TextField(_("bio"), blank=True, null=True, default=None)

    instagram = models.CharField(
        _("instagram"), max_length=64, blank=True, null=True, default=None
    )

    telegram = models.CharField(
        _("telegram"), max_length=64, blank=True, null=True, default=None
    )

    facebook = models.CharField(
        _("facebook"), max_length=254, blank=True, null=True, default=None
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        "Add default username if blank."

        super(User, self).save(*args, **kwargs)
        if not self.username:
            for i in range(123, 300000):
                username = "hunter" + str(i) + str(self.pk)
                if not User.objects.filter(username=username).exists():
                    self.username = username
                    self.save()
                    break

    def __str__(self):
        return self.email
