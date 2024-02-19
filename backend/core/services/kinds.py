from django.db.models import F, OuterRef, Subquery

from core.models.kinds import Kind, MarkerKind
from core.models.tags import TagValue


class KindService:
    @staticmethod
    def get_main_priority_kind():
        """Retrieves main kind with highest pririty."""
        return (
            KindService._get_kinds_by_class(Kind.KIND_CLASS_MAIN)
            .order_by("priority")
            .first()
        )

    @staticmethod
    def get_main_kinds():
        """Retrieves main kinds."""
        return KindService._get_kinds_by_class(Kind.KIND_CLASS_MAIN)

    @staticmethod
    def get_related_kinds():
        """Retrieves related kinds."""
        return KindService._get_kinds_by_class(Kind.KIND_CLASS_RELATED)

    @staticmethod
    def _get_suitable_kind_for_marker(marker):
        """Choose a most suitable kind by tags."""

        marker_tag_value_subquery = TagValue.objects.filter(
            value=F("value"),
            marker=marker,
            tag_id=OuterRef("tag_id"),
        ).values("id")

        return (
            Kind.objects.annotate(
                matching_tag_value=Subquery(marker_tag_value_subquery)
            )
            .order_by("priority")
            .filter(matching_tag_value__isnull=False)
            .first()
        )

    @staticmethod
    def set_marker_kind(marker):
        """
        Sets the kind for a marker if it has not been set already.

        Args:
            marker (Marker)

        Returns:
            tuple: MarkerKind instance and a boolean indicating whether a kind assigned to the marker.
        """
        marker_kinds = MarkerKind.objects.filter(marker=marker)
        if marker_kinds.exists():
            return marker_kinds.first(), False
        new_kind = KindService._get_suitable_kind_for_marker(marker)
        if new_kind:
            return MarkerKind.objects.create(marker=marker, kind=new_kind), True

    @staticmethod
    def set_marker_main_kind(marker):
        MarkerKind.objects.update_or_create(
            marker=marker,
            defaults={"kind": KindService.get_main_priority_kind()},
        )

    @staticmethod
    def _get_kinds_by_class(kind_class):
        """Retrieves kinds by class."""

        return Kind.objects.filter(kind_class=kind_class)
