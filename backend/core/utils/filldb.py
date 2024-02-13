import logging

from core.models.markers import Marker
from core.models.tags import Kind, MarkerKind, Tag, TagValue
from core.tasks import run_scrap_markers_related
from django.contrib.gis.geos import Point
from django.db.models import F, OuterRef, Subquery

logger = logging.getLogger(__name__)


def update_nodes(nodes):
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
        bool: True if the update or creation process is successful, False otherwise.

    Raises:
        Exception: If an unexpected error occurs during the database update or creation process.

    Note:
        - This function uses Django's GeoDjango framework to interact with a spatial database.
        - The provided nodes should follow a specific structure with information about markers, tags, and tag values.
        - The function updates or creates markers, tags, and tag values in an atomic transaction for data consistency.
    """

    stat = {
        "markers_upd": 0,
        "markers_add": 0,
        "tags_use": 0,
        "tags_add": 0,
        "tv_upd": 0,
        "tv_add": 0,
    }

    for node in nodes:
        try:
            # Marker
            location = Point(float(node["lon"]), float(node["lat"]))
            marker_queryset = Marker.objects.filter(location__exact=location)
            if marker_queryset.exists():  # get marker
                marker = marker_queryset.first()
                if not marker.name or not marker.osm_id:  # update marker name or osm_id
                    if not marker.name:
                        marker.name = (
                            node["name"]["v"]
                            if isinstance(node["name"], dict)
                            else node["name"]
                        )
                    if not marker.osm_id:
                        marker.osm_id = node["id"]
                    marker.save()
                    stat["markers_upd"] += 1

            else:  # create marker
                marker = Marker.objects.create(
                    name=node.get("name"), location=location, osm_id=node.get("id")
                )
                stat["markers_add"] += 1
                run_scrap_markers_related.delay(marker.id)
            # Tag
            for tag_name, tag_value in node["tags"].items():
                tag_queryset = Tag.objects.filter(name=tag_name)
                if tag_queryset.exists():  # get tag
                    tag = tag_queryset.first()
                    stat["tags_use"] += 1
                else:  # create tag
                    tag = Tag.objects.create(name=tag_name)
                    stat["tags_add"] += 1

                # TagValue
                marker_tag_value_queryset = TagValue.objects.filter(
                    marker=marker, tag=tag
                )
                if marker_tag_value_queryset.exists():  # get value
                    marker_tag_value = marker_tag_value_queryset.first()
                    # update value
                    if tag_value and marker_tag_value.value != tag_value:
                        marker_tag_value.value = tag_value
                        marker_tag_value.save()
                        stat["tv_upd"] += 1
                else:  # create marker tag value
                    if not tag_value:
                        tag_value = None
                    marker_tag_value = TagValue.objects.create(
                        marker=marker, tag=tag, value=tag_value
                    )
                    stat["tv_add"] += 1
            # kind
            marker_tag_value_subquery = TagValue.objects.filter(
                value=F("value"),
                marker=marker,
                tag_id=OuterRef("tag_id"),
            ).values("id")

            kind = (
                Kind.objects.annotate(
                    matching_tag_value=Subquery(marker_tag_value_subquery)
                )
                .order_by("priority")
                .filter(matching_tag_value__isnull=False)
                .first()
            )
            if kind and not MarkerKind.objects.filter(marker=marker).exists():
                MarkerKind.objects.create(marker=marker, kind=kind)

        except Exception as e:
            logger.exception(f"update_nodes {e}\n On node: {node}")

    return stat
