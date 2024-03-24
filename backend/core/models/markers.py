from django.contrib.gis.db import models

from core.models.kinds import Kind
from core.models.users import User


class Marker(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    location = models.PointField(null=False, blank=False, unique=True)
    osm_id = models.BigIntegerField(null=True, blank=True, default=None)

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="markers",
        verbose_name="Author",
        null=True,
        default=None,
    )
    kind = models.ForeignKey(
        Kind,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        default=None,
        related_name="marker",
        verbose_name="Marker Kind Value",
        help_text="Choice kind value for marker",
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Add date",
    )

    class Meta:
        indexes = [
            models.Index(fields=["location"]),
            models.Index(fields=["kind_id"]),
        ]

    def __str__(self):
        if not self.name:
            return str(self.id)
        return str(self.name)


class MarkerClusterMixin(models.Model):
    """Mixin for common fields in MarkerCluster and UpdatedMarkerCluster."""

    location = models.PointField(null=False, blank=False)
    square_size = models.FloatField(null=False, blank=False)
    markers_count = models.PositiveIntegerField(null=False, blank=False)

    update_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Update date",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class MarkerCluster(MarkerClusterMixin):
    """A markers cluster with count of markers for zoom."""

    class Meta:
        verbose_name_plural = "Marker Clusters"


class UpdatedMarkerCluster(MarkerClusterMixin):
    """Copy of MarkerCluster for preparing new clusters and immediately update."""

    class Meta:
        verbose_name_plural = "Updated Marker Clusters"


class RelatedMarkerScrap(models.Model):
    """To create a task for batch scraping of related markers."""

    marker = models.OneToOneField(
        Marker,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    pack_index = models.PositiveIntegerField(blank=True, null=True, default=None)
