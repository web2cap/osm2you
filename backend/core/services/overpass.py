import logging

import requests
from django.conf import settings

from core.services.kinds import KindService

logger = logging.getLogger(__name__)

OVERPASS = getattr(settings, "OVERPASS", {})
MARKERS_RELATED_IN_RADIUS = getattr(settings, "MARKERS_RELATED_IN_RADIUS", 5000)


class OverpassService:
    @staticmethod
    def overpass_main_kind_nodes(south=-90, west=-180, north=90, east=180):
        kinds = KindService.get_main_kinds()
        if not kinds.exists():
            return None

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
        return OverpassService._overpass_by_query(full_query)

    @staticmethod
    def overpass_related_nodes(location, radius=MARKERS_RELATED_IN_RADIUS):
        kinds = KindService.get_related_kinds()
        if not kinds.exists():
            return None

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
        return OverpassService._overpass_by_query(full_query)

    @staticmethod
    def _overpass_by_query(overpass_query):
        try:
            response = requests.get(OVERPASS["url"], params={"data": overpass_query})
            if response.status_code == 200:
                return response.text
            else:
                logger.error(
                    f"Overpass API response status code: {response.status_code}"
                )
                raise f"Fail with response status code: {response.status_code}"
        except Exception as e:
            logger.error(f"Overpass API error: {e}")
