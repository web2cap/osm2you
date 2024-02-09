import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from tags.models import Kind, Tag

from markers.models import Marker
from markers.tasks import run_scrap_markers_main

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Preparing for first start of application.
        Loads fixtures and add a task for scraping markers,
        if there are no any markers in the DB.
        """
        if not Tag.objects.all().exists():
            call_command("loaddata", "fixtures/tag.json")
            logger.info("Preparing tags for first start of app complete.")
        if not Kind.objects.all().exists():
            call_command("loaddata", "fixtures/kind_group.json")
            call_command("loaddata", "fixtures/kind.json")
            logger.info("Preparing kinds for first start of app complete.")
        if not Marker.objects.all().exists():
            run_scrap_markers_main.delay()
            logger.info("Task for preparing markers for first start of app complete.")
