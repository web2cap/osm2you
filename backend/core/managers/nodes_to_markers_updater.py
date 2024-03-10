import logging

from django.db import transaction
from django.db.utils import IntegrityError

from core.services.kinds import KindService
from core.services.markers import MarkerService
from core.services.related_markes_scrap import RelatedMarkerScrapService
from core.services.tags import TagStoreService, TagValueStoreService

logger = logging.getLogger(__name__)


class NodesToMarkersUpdaterManager:
    @staticmethod
    def update_markers(nodes, scrap_related=False):
        """
        Update or create markers, tags, and tag values in the database based on the provided nodes.
        Try to set kind for marker.
        Calculate statistic of changes.

        Args:
            nodes (list): A list of dictionaries representing nodes with information about markers, tags, and tag values.

                Example:
                [
                    {
                        'id': '1876313153',
                        'lat': '59.0593972',
                        'lon': '9.8729957',
                        'name': None,
                        'tags': {'backcountry': 'yes', 'impromptu': 'yes', 'tourism': 'camp_site'}
                    },
                    # ... (other nodes)
                ]
            scrap_related (bool): Flag for add task to scrape related markers

        Returns:
            dict: Report with counting of created and updated elements.
        """

        if not nodes:
            return None

        stat = {
            "markers_upd": 0,
            "markers_add": 0,
            "tags_use": 0,
            "tags_add": 0,
            "tags_values_upd": 0,
            "tags_values_add": 0,
            "kinds_add": 0,
        }
        tag_store = TagStoreService()

        for node in nodes:
            try:
                with transaction.atomic():
                    # marker
                    coordinates = {"lat": node["lat"], "lon": node["lon"]}
                    node["name"] = (
                        None
                        if node["name"] is not None and len(node["name"]) == 0
                        else node["name"]
                    )
                    node["id"] = int(node["id"]) if node["id"].isdigit() else None
                    marker = MarkerService.get_by_coordinates(coordinates)
                    if marker:
                        update_data = {}
                        if not marker.name and node["name"]:
                            update_data["name"] = node["name"]
                        if marker.osm_id != int(node["id"]):
                            update_data["osm_id"] = node["id"]
                        if len(update_data):
                            marker = MarkerService.update_marker(marker, update_data)
                            stat["markers_upd"] += 1
                    else:
                        marker, created = MarkerService.get_or_create_marker(
                            coordinates, {"name": node["name"], "osm_id": node["id"]}
                        )
                        if scrap_related and created:
                            stat["markers_add"] += 1
                            RelatedMarkerScrapService.create(marker)

                    # marker tags
                    tag_value_store = TagValueStoreService(marker)
                    for tag_name, tag_value in node["tags"].items():
                        tag, created = tag_store.get_or_create_tag(tag_name)
                        if created:
                            stat["tags_add"] += 1
                        else:
                            stat["tags_use"] += 1

                        tag_value_store.check_tag_value(tag, tag_value)

                    tags_values_add, tags_values_upd = tag_value_store.commit_values()
                    stat["tags_values_add"] += tags_values_add
                    stat["tags_values_upd"] += tags_values_upd

                    # marker kind
                    _, created = KindService.set_marker_kind(marker)
                    if created:
                        stat["kinds_add"] += 1
            except IntegrityError as e:
                logger.exception(f"IntegrityError occurred while updating nodes: {e}")
                continue
            except Exception as e:
                logger.exception(f"Error occurred while updating nodes: {e}")
                continue

        logger.info(f"Updating markers from nodes finished, with result: {stat}")
        return stat
