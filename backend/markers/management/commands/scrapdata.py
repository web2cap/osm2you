from django.conf import settings
from django.core.management.base import BaseCommand

from markers.management.utils.filldb import update_nodes
from markers.management.utils.overpass import overpass_camp_site
from markers.management.utils.scrap import scrap_nodes

SCRAPDATA_SUCCESS_MESSAGE = getattr(settings, "SCRAPDATA_SUCCESS_MESSAGE", {})
SCRAPDATA_FAILURE_MESSAGE = getattr(settings, "SCRAPDATA_FAILURE_MESSAGE", {})


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Scrap markers from openstreetmap."""

        try:
            xml_data = overpass_camp_site()
            nodes = scrap_nodes(xml_data)
            result = update_nodes(nodes)
            if result:
                self.stdout.write(
                    self.style.SUCCESS(
                        SCRAPDATA_SUCCESS_MESSAGE.format(num_records=len(nodes))
                    )
                )
            else:
                self.stdout.write(self.style.ERROR(SCRAPDATA_FAILURE_MESSAGE))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
