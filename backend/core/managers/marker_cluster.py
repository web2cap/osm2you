import logging

from django.db import transaction

from core.services.marker_cluster import MarkerClusterService

logger = logging.getLogger(__name__)


class MarkerClusterManager:
    @staticmethod
    def update_clusters():
        """
        These actions wrapped in the one transaction.
        Clears temporary table. Calculates new clusters and store them in temporary table.
        Clears production clusters table. Moves clusters from temporary table to production.
        Commits transaction.
        """
        try:
            with transaction.atomic():
                MarkerClusterService.clear_updated_marker_clusters()
                MarkerClusterService.create_clusters()
                MarkerClusterService.clear_marker_clusters()
                MarkerClusterService.copy_clusters_into_main_model()
                logger.info("Clusters updated successful.")
                return True, None
        except Exception as error:
            logger.error(f"Error updating clusters: {error}")
            return False, error
