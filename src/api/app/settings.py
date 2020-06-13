import os
from celery import Celery

SYNSPEC_PATH = os.getenv("SYNSPEC_DIRPATH")

celery_app = Celery(
    "app", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"),
)
celery_app.conf.task_routes = {"app.tasks.run_synspec": "synspec-queue"}
