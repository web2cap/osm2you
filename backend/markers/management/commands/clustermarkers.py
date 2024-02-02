import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from tags.models import Tag

from markers.models import MarkerCluster, UpdatedMarkerCluster

CLUSTERING = getattr(settings, "CLUSTERING", {})
MARKERS_KIND_MAIN = getattr(settings, "MARKERS_KIND_MAIN")

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create MarkerClusters based on Marker locations"

    def handle(self, *args, **options):
        self.clear_clusters(UpdatedMarkerCluster)
        for square_size in CLUSTERING["square_size"]:
            markers = self.create_marker_clusters(square_size)
            self.update_marker_clusters(markers, square_size)
        self.move_clusters_into_main_model()
        self.stdout.write(self.style.SUCCESS("MarkerClusters created successfully"))

    def clear_clusters(self, model):
        """Clear existing MarkerCluster data."""
        return model.objects.all().delete()

    def create_marker_clusters(self, square_size):
        """Calculate clusters for each square."""

        tourism_tag = Tag.objects.get(name=MARKERS_KIND_MAIN["tag"])
        sql_query = f"""
            SELECT ST_Centroid(ST_Collect(location)) as squared_location, COUNT(m.id) as marker_count
            FROM markers_marker as m
            LEFT JOIN tags_tagvalue tt on tt.marker_id = m.id and tt.tag_id = {tourism_tag.id}
            WHERE tt.value = '{MARKERS_KIND_MAIN["tag_value"]}'
            GROUP BY ST_SnapToGrid(location, {square_size});
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            marker_clusters = cursor.fetchall()
        return marker_clusters

    def update_marker_clusters(self, marker_clusters, square_size):
        """Save the clusters in the UpdatedMarkerCluster table."""

        for marker_cluster in marker_clusters:
            UpdatedMarkerCluster.objects.create(
                location=marker_cluster[0],
                square_size=square_size,
                markers_count=marker_cluster[1],
            )

    def move_clusters_into_main_model(self):
        """Clear MarkerCluster and copy data from UpdatedMarkerCluster to MarkerCluster."""

        if not UpdatedMarkerCluster.objects.all().count():
            raise ValueError("UpdatedMarkerCluster should not be empty.")

        self.clear_clusters(MarkerCluster)
        sql_query = """
            INSERT INTO markers_markercluster
            SELECT * FROM markers_updatedmarkercluster;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
