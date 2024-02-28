from django.conf import settings
from django.contrib.gis.db.models.functions import SnapToGrid

from core.models.markers import RelatedMarkerScrap

OVERPASS = getattr(settings, "OVERPASS", {})


class RelatedMarkerScrapService:
    """"""

    @staticmethod
    def delete_all():
        return RelatedMarkerScrap.objects.all().delete()

    @staticmethod
    def create(marker):
        return RelatedMarkerScrap.objects.create(marker=marker)

    @staticmethod
    def get_all():
        return RelatedMarkerScrap.objects.all()

    @staticmethod
    def get_all_squares():
        markers = RelatedMarkerScrap.objects.select_related("marker").annotate(
            grid=SnapToGrid("marker__location", OVERPASS["related"]["square_size"])
        )
        markers_by_squares = {}
        for marker in markers:
            gindex = f"{marker.grid.x}{marker.grid.y}"
            if gindex not in markers_by_squares:
                markers_by_squares[gindex] = []
            markers_by_squares[gindex].append(marker)
        return markers_by_squares
