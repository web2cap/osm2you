import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task
def run_clustermarkers():
    call_command("clustermarkers")


@shared_task
def run_scrap_markers_main():
    call_command("scrapdata", "main")
    run_clustermarkers.delay()
