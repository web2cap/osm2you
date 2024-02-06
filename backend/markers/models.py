from django.contrib.gis.db import models
from users.models import User


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
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Add date",
    )

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
