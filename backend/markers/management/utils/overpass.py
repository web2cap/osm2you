import logging

import requests
from django.conf import settings

OVERPASS = getattr(settings, "OVERPASS", {})
logger = logging.getLogger(__name__)


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

    params = {
        "data": OVERPASS["camp_site"].format(
            south=south, west=west, north=north, east=east
        )
    }
    try:
        response = requests.get(OVERPASS["url"], params=params)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        logger.error(f"overpass_camp_site {e}")
    else:
        logger.error(f"overpass_camp_site response {response.status_code}")
        return None
