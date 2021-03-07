import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_api.settings")
app = Celery("tasks_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
