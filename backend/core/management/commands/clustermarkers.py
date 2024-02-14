from django.core.management.base import BaseCommand

from core.managers.marker_cluster import MarkerClusterManager


class Command(BaseCommand):
    help = "Update MarkerClusters based on Marker locations"

    def handle(self, *args, **options):
        status, code = MarkerClusterManager.update_clusters()
        if status:
            self.stdout.write(
                self.style.SUCCESS("Markers clusters updated successfully.")
            )
        else:
            self.stdout.write(self.style.ERROR(code))
