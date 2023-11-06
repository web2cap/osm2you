from django.contrib.gis.db import models
from users.models import User


class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255, null=False, blank=False)
    location = models.PointField(null=False, blank=False, unique=True)

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
        return self.name
