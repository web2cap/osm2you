import logging

import requests
from django.conf import settings

from core.services.kinds import KindService

logger = logging.getLogger(__name__)

OVERPASS = getattr(settings, "OVERPASS", {})
MARKERS_RELATED_IN_RADIUS = getattr(settings, "MARKERS_RELATED_IN_RADIUS", 5000)


class OverpassService:
    def __init__(self):
        self.overpass_url = OVERPASS.get("url")
        self.main_subquery_wrap = OVERPASS.get("main", {}).get("wrap")
        self.main_subquery_template = OVERPASS.get("main", {}).get("subquery")
        self.related_subquery_wrap = OVERPASS.get("related", {}).get("wrap")
        self.related_subquery_template = OVERPASS.get("related", {}).get("subquery")

    def _overpass_by_query(self, overpass_query):
        try:
            response = requests.get(self.overpass_url, params={"data": overpass_query})
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.error(f"Overpass API error: {e}")
        else:
            logger.error(f"Overpass API response status code: {response.status_code}")
            return None

    def overpass_camp_site(self, south=-90, west=-180, north=90, east=180):
        kinds = KindService.get_main_kinds()
        if not kinds.exists():
            return None

        subqueries = []
        for kind in kinds:
            subquery = self.main_subquery_template.format(
                tag_name=kind.tag,
                tag_value=kind.value,
                south=south,
                west=west,
                north=north,
                east=east,
            )
            subqueries.append(subquery)

        full_query = self.main_subquery_wrap.format(subqueries="".join(subqueries))
        return self._overpass_by_query(full_query)

    def overpass_related(self, location, radius=MARKERS_RELATED_IN_RADIUS):
        kinds = KindService.get_related_kinds()
        if not kinds.exists():
            return None

        subqueries = []
        for kind in kinds:
            subquery = self.related_subquery_template.format(
                tag_name=kind.tag,
                tag_value=kind.value,
                radius=radius,
                lat=location[1],
                lon=location[0],
            )
            subqueries.append(subquery)

        full_query = self.related_subquery_wrap.format(subqueries="".join(subqueries))
        return self._overpass_by_query(full_query)
