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
        for square_size in CLUSTERING["square_size"]:
            markers = self.create_marker_clusters(square_size)
            self.clear_marker_clusters(square_size)
            self.update_marker_clusters(markers, square_size)

        self.stdout.write(self.style.SUCCESS("MarkerClusters created successfully"))

    def clear_marker_clusters(self, square_size):
        """Clear existing MarkerCluster data."""
        if not square_size:
            return False

        return MarkerCluster.objects.filter(square_size=square_size).delete()

    def create_marker_clusters(self, square_size):
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

    def update_marker_clusters(self, marker_clusters, square_size):
        """Save the clusters in the MarkerCluster table."""

        for marker_cluster in marker_clusters:
            MarkerCluster.objects.create(
                location=marker_cluster[0],
                square_size=square_size,
                markers_count=marker_cluster[1],
            )
