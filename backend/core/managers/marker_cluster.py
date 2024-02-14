import logging

from django.db import transaction

from core.services.marker_cluster import MarkerClusterService

logger = logging.getLogger(__name__)


class MarkerClusterManager:
    @staticmethod
    def update_clusters():
        """Wraps the operations of updating marker clusters in a single transaction.
        It calls methods from MarkerClusterService to clear temporary marker clusters.
        Then create new clusters, clear production clusters, move clusters from temporary to production.
        It logs any errors that occur during the process.
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
