from django.db import models

from core.models.kinds import Kind
from core.models.markers import Marker


class MarkerKind(models.Model):
    kind = models.ForeignKey(
        Kind,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="marker_kind_value",
        verbose_name="Marker Kind Value",
        help_text="Choice kind value for marker",
    )
    marker = models.OneToOneField(
        Marker,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="marker_kind",
        verbose_name="Marker",
        help_text="Choice marker",
    )

    class Meta:
        verbose_name = "Marker kind value"
        verbose_name_plural = "Markers kind value"

    def __str__(self):
        return f"{self.marker.name} [{self.kind}]"
