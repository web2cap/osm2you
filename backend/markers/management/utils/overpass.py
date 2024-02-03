import logging

import requests
from django.conf import settings

OVERPASS = getattr(settings, "OVERPASS", {})
MARKERS_KIND_MAIN = getattr(settings, "MARKERS_KIND_MAIN", {})

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
    overpass_query = OVERPASS["main"].format(
        tag=f"{MARKERS_KIND_MAIN['tag']}={MARKERS_KIND_MAIN['tag_value']}",
        south=south,
        west=west,
        north=north,
        east=east,
    )
    return overpass_by_query(overpass_query)
