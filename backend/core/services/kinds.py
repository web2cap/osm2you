from django.db.models import F, OuterRef, Subquery

from core.models.kinds import Kind
from core.models.tag_values import TagValue


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
    def get_related_kinds_dict():
        """Retrieves related kinds in the dict."""

        kinds = KindService.get_related_kinds()
        if not kinds.exists():
            return None
        kinds_dict = {}
        for kind in kinds:
            if kind.tag not in kinds_dict:
                kinds_dict[kind.tag] = []
            kinds_dict[kind.tag].append(kind.value)

        return kinds_dict

    @staticmethod
    def get_kinds_all():
        return Kind.objects.all()

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
            tuple: Marker instance and a boolean indicating whether a kind assigned to the marker.
        """

        if not marker.kind:
            new_kind = KindService._get_suitable_kind_for_marker(marker)
            if new_kind:
                marker.kind = new_kind
                marker.save()
                return marker, True
        return marker, False

    @staticmethod
    def set_marker_main_kind(marker):
        marker.kind = KindService.get_main_priority_kind()
        marker.save()

    @staticmethod
    def _get_kinds_by_class(kind_class):
        """Retrieves kinds by class."""

        return Kind.objects.filter(kind_class=kind_class).select_related("tag")
