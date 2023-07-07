from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models
from markers.models import Marker

User = get_user_model()


class Story(CreatedModel):
    text = models.TextField(verbose_name="Text", help_text="Write you story")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories",
        verbose_name="Author",
    )
    marker = models.ForeignKey(
        Marker,
        on_delete=models.SET(0),
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

    def __str__(self) -> str:
        return self.text[:15]
