from django.db import models
from django.db.models import Q, TextField
from django.db.models.functions import Length

from core.models.create import CreatedModel
from core.models.markers import Marker
from core.models.users import User

TextField.register_lookup(Length, "length")


class Story(CreatedModel):
    text = models.TextField(
        verbose_name="Text", help_text="Write you story", null=False, blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories",
        verbose_name="Author",
        null=False,
        blank=False,
    )
    marker = models.ForeignKey(
        Marker,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="stories",
        verbose_name="Marker",
        help_text="Choice marker",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Story"
        verbose_name_plural = "Stories"
        constraints = [
            models.CheckConstraint(
                check=Q(text__length__gte=10),
                name="text_min_length",
            )
        ]

    def __str__(self) -> str:
        return self.text[:15]
