from django.conf import settings
from django.db import connection

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
        square_size = OVERPASS["related"]["square_size"]
        sql_query = f"""
            SELECT cm."location", ST_SnapToGrid(location, {square_size}) grid	
            FROM core_relatedmarkerscrap cr
            LEFT JOIN core_marker cm ON cm.id = cr.marker_id 
            ORDER BY grid;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            all_squares = cursor.fetchall()

        return all_squares
