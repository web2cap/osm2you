from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "osm2you.settings")

app = Celery("osm2you")  # , include=["osm2you.markers.tasks"])
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(settings.INSTALLED_APPS)
app.autodiscover_tasks()

app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

app.conf.beat_schedule = {
    "run_scrapdata": {
        # Run every night at 2 AM
        "task": "markers.tasks.run_scrapdata",
        "schedule": crontab(minute=10, hour=19),
    },
    "run_sleeper": {
        # Run every 5 min TEST
        "task": "markers.tasks.run_sleeper",
        "schedule": crontab(minute="*/5"),
    },
}

app.conf.timezone = "UTC"
