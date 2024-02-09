import logging

import requests
from django.conf import settings
from tags.models import Kind

OVERPASS = getattr(settings, "OVERPASS", {})
MARKERS_KIND_MAIN = getattr(settings, "MARKERS_KIND_MAIN", {})
MARKERS_RELATED_IN_RADIUS = getattr(settings, "MARKERS_RELATED_IN_RADIUS", 5000)

logger = logging.getLogger(__name__)


def overpass_by_query(overpass_query):
    """
    Query the Overpass API with prepeared query.

    Args:
        overpass_query (str): overpass API query.
    Returns:
        str or None: Overpass API response text if successful, None otherwise.
    """

    try:
        response = requests.get(OVERPASS["url"], params={"data": overpass_query})
        if response.status_code == 200:
            return response.text
    except Exception as e:
        logger.error(f"overpass {e}")
    else:
        logger.error(f"overpass response {response.status_code}")
        return None


def overpass_camp_site(south=-90, west=-180, north=90, east=180):
    """
    Query the Overpass API for campsite data within a specified bounding box.

    Args:
        south (float): Southern latitude limit (default: -90).
        west (float): Western longitude limit (default: -180).
        north (float): Northern latitude limit (default: 90).
        east (float): Eastern longitude limit (default: 180).

    Returns:
        str or None: Overpass API response text if successful, None otherwise.

    Note:
        - The bounding box is defined by the parameters (south, west, north, east).
        - The Overpass API URL and query template are fetched from the Django settings.
    """
    kinds = Kind.objects.filter(kind_class=Kind.KIND_CLASS_MAIN)
    if not kinds.exists():
        return False

    subqueries = []
    for kind in kinds:
        subquery = OVERPASS["main"]["subquery"].format(
            tag_name=kind.tag,
            tag_value=kind.value,
            south=south,
            west=west,
            north=north,
            east=east,
        )
        subqueries.append(subquery)

    full_query = OVERPASS["main"]["wrap"].format(subqueries="".join(subqueries))
    return overpass_by_query(full_query)


def overpass_related(location, radius=MARKERS_RELATED_IN_RADIUS):
    """
    Query the Overpass API for related markers data within a specified radius.

    Args:
        location (list[float,float]): Location of main marker.
        rqadius (int): Radius around main marker for searching related markers.

    Returns:
        str or None: Overpass API response text if successful, None otherwise.
    """
    kinds = Kind.objects.filter(kind_class=Kind.KIND_CLASS_RELATED)
    if not kinds.exists():
        return False

    subqueries = []
    for kind in kinds:
        subquery = OVERPASS["related"]["subquery"].format(
            tag_name=kind.tag,
            tag_value=kind.value,
            radius=radius,
            lat=location[1],
            lon=location[0],
        )
        subqueries.append(subquery)

    full_query = OVERPASS["related"]["wrap"].format(subqueries="".join(subqueries))
    return overpass_by_query(full_query)
