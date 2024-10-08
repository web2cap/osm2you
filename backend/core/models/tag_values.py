from django.db import models
from django.db.models import Q

from core.models.create import CreatedModel
from core.models.markers import Marker
from core.models.tags import Tag


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
            models.UniqueConstraint(
                fields=["tag", "marker"],
                name="unique_marker_tag",
            ),
            models.CheckConstraint(
                check=Q(value__length__gte=1),
                name="value_min_length",
            ),
        ]

    def __str__(self):
        return self.tag.name
