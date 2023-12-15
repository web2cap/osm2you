from core.models import CreatedModel
from django.db import models
from django.db.models import CharField, Q
from django.db.models.functions import Length
from markers.models import Marker

CharField.register_lookup(Length, "length")


class Tag(CreatedModel):
    """Tags clasifficator with human-friendly name"""

    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    display_name = models.CharField(
        max_length=255, null=True, blank=False, default=None
    )

    class Meta:
        ordering = ("-name",)
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        constraints = [
            models.CheckConstraint(
                check=Q(name__length__gte=1),
                name="name_min_length",
            )
        ]

    def __str__(self):
        return self.name


class TagValue(CreatedModel):
    """Tags values for marker"""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="tag_value",
        verbose_name="Tag",
        help_text="Specify value for tag",
    )
    marker = models.ForeignKey(
        Marker,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="tag_value",
        verbose_name="Marker",
        help_text="Choice marker",
    )
    value = models.CharField(max_length=255, null=True, blank=False, default=None)

    class Meta:
        ordering = ("-tag",)
        verbose_name = "Tag value"
        verbose_name_plural = "Tags values"
        constraints = [
            models.CheckConstraint(
                check=Q(value__length__gte=1),
                name="value_min_length",
            )
        ]

    def __str__(self):
        return self.tag
