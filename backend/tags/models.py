from core.models import CreatedModel
from django.db import models
from django.db.models import CharField, Q
from django.db.models.functions import Length

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
