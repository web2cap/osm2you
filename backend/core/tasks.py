import logging
import time
import random

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


@shared_task(rate_limit="60/m", bind=True, max_retries=3)
def run_scrap_markers_pack(self, pack_index):
    try:
        call_command("scrapemarkers", "related", pack=pack_index)
    except Exception as e:
        logger.warning(e)
        self.retry(exc=e, countdown=3)
