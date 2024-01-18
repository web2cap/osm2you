from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "osm2you.settings")

app = Celery("osm2you")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run_scrapdata": {
        # Run every night at 2 AM
        "task": "osm2you.tasks.run_scrapdata",
        "schedule": crontab(minute=0, hour=2),
    },
}

app.conf.timezone = "UTC"
