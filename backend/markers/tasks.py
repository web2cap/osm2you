import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)

from time import sleep


@shared_task
def run_clustermarkers():
    call_command("clustermarkers")


@shared_task
def run_scrapdata():
    call_command("scrapdata")
    run_clustermarkers.delay()


@shared_task
def run_makemigration():
    call_command("makemigration")
    logger.warning("Makemigration completed")


@shared_task
def run_sleeper():
    sleep(120)
    logger.warning("Sleep completed")
