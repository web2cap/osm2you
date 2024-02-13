from django.db import models
from django.db.models import CharField, Q
from django.db.models.functions import Length

from core.models.create import CreatedModel
from core.models.markers import Marker

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
    """Group to generalize the kind of markers."""

    ICON_CHOICES = (
        ("fa-car", "Car"),
        ("fa-bicycle", "Bicycle"),
        ("fa-bus", "Bus"),
        ("fa-train", "Train"),
        ("fa-subway", "Subway"),
        ("fa-truck", "Truck"),
        ("fa-motorcycle", "Motorcycle"),
        ("fa-plane", "Plane"),
        ("fa-ship", "Ship"),
        ("fa-space-shuttle", "Space Shuttle"),
        ("fa-shopping-cart", "Shopping Cart"),
        ("fa-shopping-bag", "Shopping Bag"),
        ("fa-money", "Money"),
        ("fa-credit-card", "Credit Card"),
        ("fa-bank", "Bank"),
        ("fa-wrench", "Wrench"),
        ("fa-tools", "Tools"),
        ("fa-medkit", "Medkit"),
        ("fa-ambulance", "Ambulance"),
        ("fa-fire-extinguisher", "Fire Extinguisher"),
        ("fa-life-ring", "Life Ring"),
        ("fa-life-saver", "Life Saver"),
        ("fa-heartbeat", "Heartbeat"),
        ("fa-heart", "Heart"),
        ("fa-smile", "Smile"),
        ("fa-frown", "Frown"),
        ("fa-meh", "Meh"),
        ("fa-grin", "Grin"),
        ("fa-trophy", "Trophy"),
        ("fa-futbol", "Soccer Ball"),
        ("fa-baseball-ball", "Baseball"),
        ("fa-basketball-ball", "Basketball"),
        ("fa-football-ball", "Football"),
        ("fa-golf-ball", "Golf Ball"),
        ("fa-hockey-puck", "Hockey Puck"),
        ("fa-volleyball-ball", "Volleyball"),
        ("fa-bowling-ball", "Bowling Ball"),
        ("fa-paw", "Paw"),
        ("fa-leaf", "Leaf"),
        ("fa-tree", "Tree"),
        ("fa-seedling", "Seedling"),
        ("fa-cogs", "Cogs"),
        ("fa-globe", "Globe"),
        ("fa-map", "Map"),
        ("fa-compass", "Compass"),
        ("fa-road", "Road"),
        ("fa-diamond", "Diamond"),
        ("fa-cut", "Cut"),
        ("fa-graduation-cap", "Graduation Cap"),
        ("fa-school", "School"),
        ("fa-university", "University"),
        ("fa-book", "Book"),
        ("fa-pencil", "Pencil"),
        ("fa-microphone", "Microphone"),
        ("fa-music", "Music"),
        ("fa-video", "Video"),
        ("fa-image", "Image"),
        ("fa-camera", "Camera"),
        ("fa-headphones", "Headphones"),
        ("fa-phone", "Phone"),
        ("fa-envelope", "Envelope"),
        ("fa-comments", "Comments"),
        ("fa-comment", "Comment"),
        ("fa-user", "User"),
        ("fa-users", "Users"),
        ("fa-group", "Group"),
        ("fa-lock", "Lock"),
        ("fa-key", "Key"),
        ("fa-cog", "Cog"),
        ("fa-exclamation", "Exclamation"),
    )

    COLOR_CHOICES = (
        ("blue", "Blue"),
        ("red", "Red"),
        ("green", "Green"),
        ("purple", "Purple"),
        ("orange", "Orange"),
        ("yellow", "Yellow"),
        ("pink", "Pink"),
        ("cyan", "Cyan"),
        ("teal", "Teal"),
        ("lime", "Lime"),
        ("brown", "Brown"),
        ("grey", "Grey"),
        ("black", "Black"),
        ("white", "White"),
    )

    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    descriptive_name = models.CharField(max_length=128, null=True, blank=False)
    icon = models.CharField(
        max_length=100, choices=ICON_CHOICES, null=False, blank=False, default="fa-leaf"
    )
    color = models.CharField(
        max_length=20, choices=COLOR_CHOICES, null=False, blank=False, default="green"
    )

    class Meta:
        ordering = ("-name",)
        verbose_name = "Kind group"
        verbose_name_plural = "Kinds groups"

    def __str__(self):
        return self.name


class Kind(models.Model):
    """Unique kinds in tag=value format, with classification by kind groups.
    Every kind has kind_class main or related."""

    KIND_CLASS_MAIN = "main"
    KIND_CLASS_RELATED = "related"
    KIND_CLASS_CHOICES = (
        (KIND_CLASS_MAIN, "main"),
        (KIND_CLASS_RELATED, "related"),
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
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="kind_tag",
        verbose_name="Kind tag",
        help_text="Choice tag for describe kind",
    )
    kind_class = models.CharField(
        max_length=32,
        choices=KIND_CLASS_CHOICES,
        blank=False,
        null=False,
        default=KIND_CLASS_RELATED,
        verbose_name="Kind class",
        help_text="Choice class for this kind",
    )
    priority = models.SmallIntegerField(
        blank=False,
        null=False,
        default=2,
        verbose_name="Kind priority",
        help_text="Fill priority for this kind property",
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
    marker = models.OneToOneField(
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

    def __str__(self):
        return f"{self.marker.name} [{self.kind}]"
