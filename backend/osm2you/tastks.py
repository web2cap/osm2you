from celery import shared_task
from django.core.management import call_command


@shared_task
def run_clustermarkers():
    call_command("clustermarkers")


@shared_task
def run_scrapdata():
    call_command("scrapdata")
    run_clustermarkers.delay()
