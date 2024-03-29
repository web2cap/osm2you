import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.services.kinds import KindService
from core.services.markers import MarkerService
from core.services.tags import TagService
from core.tasks import run_scrap_markers_main

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Command for preparing the application for first start.
    Loads fixtures and adds a task for scraping markers if necessary.
    """

    def handle(self, *args, **options):
        """Handle command execution."""
        self.load_tags()
        self.load_kinds()
        self.scrape_markers()

    def load_tags(self):
        """Load tags if they don't exist in the database."""
        if not TagService.get_tags_all().exists():
            call_command("loaddata", "fixtures/tag.json")
            logger.info("Tags loaded for first start of app.")

    def load_kinds(self):
        """Load kinds if they don't exist in the database."""
        if not KindService.get_kinds_all().exists():
            call_command("loaddata", "fixtures/kind_group.json")
            call_command("loaddata", "fixtures/kind.json")
            logger.info("Kinds loaded for first start of app.")

    def scrape_markers(self):
        """Create task for scrape markers if they don't exist in the database."""
        if not MarkerService.get_markers_all().exists():
            run_scrap_markers_main.delay()
            logger.info("Task for scraping markers scheduled for first start of app.")
