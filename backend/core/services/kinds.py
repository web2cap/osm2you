from core.models.tags import Kind


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
    def _get_kinds_by_class(kind_class):
        """Retrieves kinds by class."""

        return Kind.objects.filter(kind_class=kind_class)
