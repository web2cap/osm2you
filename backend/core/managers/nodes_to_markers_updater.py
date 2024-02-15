import logging

from django.db import transaction
from django.db.utils import IntegrityError

from core.services.kinds import KindService
from core.services.markers import MarkerService
from core.services.tags import TagService
from core.tasks import run_scrap_markers_related

logger = logging.getLogger(__name__)


class NodesToMarkersUpdaterManager:

    @classmethod
    def update_markers(nodes):
        """
        Update or create markers, tags, and tag values in the database based on the provided nodes.

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

        Returns:
            dict: Report with counting of created and updated elements.
        """

        stat = {
            "markers_upd": 0,
            "markers_add": 0,
            "tags_use": 0,
            "tags_add": 0,
            "tags_values_upd": 0,
            "tags_values_add": 0,
            "kinds_add": 0,
        }
        for node in nodes:
            try:
                with transaction.atomic():
                    # marker
                    coordinates = {"lat": node["lat"], "lon": node["lon"]}
                    marker_data = {
                        "name": node["name"],
                        "osm_id": node["id"],
                    }
                    marker, created = MarkerService.get_or_create_marker(
                        coordinates, marker_data
                    )
                    if created:
                        stat["markers_add"] += 1
                        run_scrap_markers_related.delay(marker.id)

                    elif (not marker.name and "name" in marker_data) or (
                        not marker.osm_id and "name" in marker_data
                    ):
                        if "name" in marker_data and marker.name:
                            marker_data.pop("name")
                        marker = MarkerService.update_marker(marker, marker_data)
                        stat["markers_upd"] += 1

                    # marker tags
                    for tag_name, tag_value in node["tags"].items():
                        tag, created = TagService.get_or_create_tag(tag_name)
                        if created:
                            stat["tags_add"] += 1
                        else:
                            stat["tags_use"] += 1

                        marker_tag_value, created = (
                            TagService.update_or_create_tag_value(
                                tag, tag_value, marker
                            )
                        )
                        if (
                            not created
                            and tag_value
                            and marker_tag_value.value != tag_value
                        ):
                            marker_tag_value.value = tag_value
                            marker_tag_value.save()
                            stat["tags_values_upd"] += 1
                        elif created:
                            stat["tags_values_add"] += 1

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
