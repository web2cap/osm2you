import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

from markers.models import Marker
from markers.tasks import run_scrapdata

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Preparing for first start of application.
        Loads fixtures and add a task for scraping markers,
        if there are no any markers in the DB.
        """
        if not Marker.objects.all().exists():
            call_command("loaddata", "fixtures/tag.json")
            run_scrapdata.delay()
            logger.info("Preparing for first start of app complete.")
