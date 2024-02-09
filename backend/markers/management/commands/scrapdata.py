import logging
import sys

from django.core.management.base import BaseCommand

from markers.management.utils.filldb import update_nodes
from markers.management.utils.overpass import overpass_camp_site, overpass_related
from markers.management.utils.scrap import scrap_nodes
from markers.models import Marker

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "scenario", choices=["main", "related"], help="Choose the scenario."
        )
        parser.add_argument(
            "--id", type=int, help="Specify the marker id for 'related' scenario."
        )

    def handle(self, *args, **options):
        """Scrap markers from openstreetmap.org by using overpass-turbo.eu.
        Fills markers and tags with them values into database.
        Logs the main steps."""

        scenario = options["scenario"]
        id = options.get("id", None)

        try:
            if scenario == "main":
                xml_data = overpass_camp_site()
            elif scenario == "related":
                if not id:
                    raise ("Main marker id is required for 'related' scenario.")
                marker = Marker.objects.get(id=id)
                xml_data = overpass_related(marker.location)
            else:
                raise ("Invalid scenario. Choose 'main' or 'related'.")
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
