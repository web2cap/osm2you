from core.models import CreatedModel
from django.db import models


class Tag(CreatedModel):
    """Tags clasifficator with human-friendly name"""

    name = models.CharField(max_length=255, null=False, blank=False)
    display_name = models.CharField(
        max_length=255, null=True, blank=False, default=None
    )

    def __str__(self):
        return self.name
