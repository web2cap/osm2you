from django.contrib.gis.db import models
from users.models import User


class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255)
    location = models.PointField()

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="markers",
        verbose_name="Author",
        null=True,
        default=None,
    )

    def __str__(self):
        return self.name
