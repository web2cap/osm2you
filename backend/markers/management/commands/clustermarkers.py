import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

from markers.models import MarkerCluster

CLUSTERING = getattr(settings, "CLUSTERING", {})

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create MarkerClusters based on Marker locations"

    def handle(self, *args, **options):
        clusters_kinds = zip(CLUSTERING["square_size"], CLUSTERING["zoom"])
        for size, zoom in clusters_kinds:
            markers = self.create_marker_clusters(size, zoom)
            self.clear_marker_clusters(zoom)
            self.update_marker_clusters(markers, size, zoom)

        self.stdout.write(self.style.SUCCESS("MarkerClusters created successfully"))

    def clear_marker_clusters(self, zoom):
        """Clear existing MarkerCluster data."""
        if not zoom:
            return False

        return MarkerCluster.objects.filter(zoom=zoom).delete()

    def create_marker_clusters(self, square_size, zoom_level):
        """Calculate clusters for each square."""

        sql_query = f"""
            SELECT ST_SnapToGrid(location, {square_size}) as squared_location, COUNT(id) as marker_count
            FROM markers_marker
            GROUP BY ST_SnapToGrid(location, {square_size})
            ORDER BY squared_location;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            marker_clusters = cursor.fetchall()
        return marker_clusters

    def update_marker_clusters(self, marker_clusters, square_size, zoom_level):
        """Save the clusters in the MarkerCluster table."""

        for marker_cluster in marker_clusters:
            MarkerCluster.objects.create(
                location=marker_cluster[0],
                zoom=zoom_level,
                markers_count=marker_cluster[1],
            )
