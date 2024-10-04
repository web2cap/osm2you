from celery import Celery
from django.conf import settings


def test_celery_config():
    app = Celery()
    app.config_from_object(settings)

    assert app.conf.CELERY_BROKER_URL == settings.CELERY_BROKER_URL
    assert app.conf.CELERY_RESULT_BACKEND == settings.CELERY_RESULT_BACKEND
    assert app.conf.CELERY_ACCEPT_CONTENT == settings.CELERY_ACCEPT_CONTENT
    assert app.conf.CELERY_TASK_SERIALIZER == settings.CELERY_TASK_SERIALIZER
    assert app.conf.CELERY_RESULT_SERIALIZER == settings.CELERY_RESULT_SERIALIZER
    assert app.conf.CELERY_TIMEZONE == settings.CELERY_TIMEZONE
    assert app.conf.CELERY_BEAT_SCHEDULER == settings.CELERY_BEAT_SCHEDULER
    assert app.conf.CELERY_BEAT_SCHEDULE == settings.CELERY_BEAT_SCHEDULE


def test_celery_autodiscover_tasks():
    app = Celery()
    app.config_from_object(settings)
    app.autodiscover_tasks()

    assert len(app.tasks) > 0
