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


class KindGroup(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    descriptive_name = models.CharField(max_length=128, null=True, blank=False)

    class Meta:
        ordering = ("-name",)
        verbose_name = "Kind group"
        verbose_name_plural = "Kinds groups"

    def __str__(self):
        return self.name


class Kind(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="kind_tag",
        verbose_name="Kind tag",
        help_text="Choice tag for describe kind",
    )
    kind_group = models.ForeignKey(
        KindGroup,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="kind_tag",
        verbose_name="Kind Group",
        help_text="Specify kind group",
    )
    value = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        ordering = ("-tag", "-value")
        verbose_name = "Marker kind"
        verbose_name_plural = "Markers kinds"
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "value"],
                name="unique_kind_tag",
            )
        ]

    def __str__(self):
        return f"{self.tag.name}={self.value}"


class MarkerKind(models.Model):
    kind = models.ForeignKey(
        Kind,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="kind_value",
        verbose_name="Marker Kind Value",
        help_text="Choice kind value for marker",
    )
    marker = models.ForeignKey(
        Marker,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="kind",
        verbose_name="Marker",
        help_text="Choice marker",
    )

    class Meta:
        verbose_name = "Marker kind value"
        verbose_name_plural = "Markers kind value"
        constraints = [
            models.UniqueConstraint(
                fields=["kind", "marker"],
                name="unique_kind_marker_value",
            )
        ]

    def __str__(self):
        return f"{self.marker.name} [{self.kind}]"
