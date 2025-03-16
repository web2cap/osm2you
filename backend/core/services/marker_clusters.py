from django.conf import settings
from django.db import connection

from core.models.kinds import Kind
from core.models.markers import MarkerCluster, UpdatedMarkerCluster

CLUSTERING = getattr(settings, "CLUSTERING", {})


class MarkerClusterService:
    """Handles the retrive,  creation, copying, and clearing of marker clusters.
    It provides methods for creating and clearing clusters, copying clusters into the main model.
    """

    @staticmethod
    def get_clusters_by_size(square_size):
        if not square_size:
            raise ValueError("Specify square_size for retrive")
        return MarkerCluster.objects.filter(square_size=square_size)

    @staticmethod
    def create_clusters():
        """Creates clusters for all square_size and store it to temporary UpdatedMarkerCluster."""
        for square_size in CLUSTERING["square_size"]:
            marker_clusters = MarkerClusterService._calculate_marker_clusters(
                square_size
            )
            MarkerClusterService._save_marker_clusters(marker_clusters, square_size)

    @staticmethod
    def copy_clusters_into_main_model():
        """Copy all data from temporary UpdatedMarkerCluster to production MarkerCluster."""
        sql_query = """
            INSERT INTO core_markercluster
            SELECT * FROM core_updatedmarkercluster;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query)

    @staticmethod
    def clear_marker_clusters():
        """Clear existing MarkerCluster data."""
        return MarkerCluster.objects.all().delete()

    @staticmethod
    def clear_updated_marker_clusters():
        """Clear existing UpdatedMarkerCluster data."""
        return UpdatedMarkerCluster.objects.all().delete()

    @staticmethod
    def _calculate_marker_clusters(square_size):
        """Calculate markers count for each square with setted size in the map.
        Calculate averege position of markers for every sqare like a marker cluster position.
        """
        sql_query = f"""
        SELECT ST_Centroid(ST_Collect(location)) as squared_location, COUNT(m.id) as marker_count
            FROM core_marker as m 
            LEFT JOIN core_kind tk on tk.id = m.kind_id 
            WHERE tk.kind_class  = '{Kind.KIND_CLASS_MAIN}'
            GROUP BY ST_SnapToGrid(location, {square_size});
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            marker_clusters = cursor.fetchall()

        return marker_clusters

    @staticmethod
    def _save_marker_clusters(marker_clusters, square_size):
        """Save markers clusters into temporary UpdatedMarkerCluster."""
        for marker_cluster in marker_clusters:
            UpdatedMarkerCluster.objects.create(
                location=marker_cluster[0],
                square_size=square_size,
                markers_count=marker_cluster[1],
            )
