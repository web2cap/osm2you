import logging
import sys

from django.core.management.base import BaseCommand

from markers.management.utils.filldb import update_nodes
from markers.management.utils.overpass import overpass_camp_site
from markers.management.utils.scrap import scrap_nodes

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Scrap markers from openstreetmap.org by using overpass-turbo.eu.
        Fills markers and tags with them values into database.
        Logs the main steps."""

        try:
            logger.warning("Start loading overpass xml data")
            xml_data = overpass_camp_site(south=0, west=0, north=90, east=180)
            xml_data_size = sys.getsizeof(xml_data) / 1024
            logger.warning(f"XML loadded, size {xml_data_size:.2f} KB")
            logger.warning("Start scrapping xml data")
            nodes = scrap_nodes(xml_data)
            logger.warning(f"Nodes loadded, size {len(nodes)}")
            logger.warning("Start filling nodes")
            result = update_nodes(nodes)
            logger.warning(f"Nodes updated, stat: {result}")
        except Exception as e:
            logger.exception(f"Scrapdata error {e}")
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
