import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task
def run_clustermarkers():
    call_command("clustermarkers")


@shared_task
def run_scrap_markers_main():
    call_command("scrapemarkers", "main")


@shared_task
def run_scrap_markers_related(marker_id):
    call_command("scrapemarkers", "related", id=marker_id)


@shared_task
def run_scrap_markers_batch_related():
    call_command("scrapemarkers", "related")
