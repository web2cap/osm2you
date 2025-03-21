from django.conf import settings
from django.contrib.gis.db.models.functions import SnapToGrid
from django.db.models import Max

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
    def get_by_pack_index(pack_index):
        return RelatedMarkerScrap.objects.filter(pack_index=pack_index)

    @staticmethod
    def delete_pack(markers):
        for marker in markers:
            marker.delete()

    @staticmethod
    def get_all_squares_by_pack():
        """Divides markers into square areas and packages within each area.

        Returns:
            dict: A dictionary with markers divided into square areas.
            Each square area contains packages of markers, where each package
            contains markers no larger than the specified package size.


        Returns:
            dict: A dictionary where keys represent square areas (identified by grid indices),
            and values are lists of packages, each containing markers.
        """
        markers = (
            RelatedMarkerScrap.objects.select_related("marker")
            .annotate(
                grid=SnapToGrid(
                    "marker__location", OVERPASS["related_batch"]["square_size"]
                )
            )
            .order_by("grid")
        )
        markers_by_squares = {}
        for marker in markers:
            grid_index = f"{marker.grid.x}_{marker.grid.y}"
            if grid_index not in markers_by_squares:
                markers_by_squares[grid_index] = []
                grid_element_index = 0
            if grid_element_index % OVERPASS["related_batch"]["packege_size"] == 0:
                markers_by_squares[grid_index].append([])
                pack_index = len(markers_by_squares[grid_index]) - 1
            markers_by_squares[grid_index][pack_index].append(marker)
            grid_element_index += 1

        return markers_by_squares

    @staticmethod
    def get_next_free_pack_index():
        max_pack_index = RelatedMarkerScrap.objects.aggregate(Max("pack_index"))[
            "pack_index__max"
        ]
        if max_pack_index:
            return max_pack_index + 1
        return 1

    @staticmethod
    def set_pack_index(markers, pack_index):
        marker_ids = [marker.id for marker in markers]
        RelatedMarkerScrap.objects.filter(id__in=marker_ids).update(
            pack_index=pack_index
        )
