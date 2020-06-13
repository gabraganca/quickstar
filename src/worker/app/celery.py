from celery import Celery

from app.settings import CELERY_BACKEND_URL, CELERY_BROKER_URL

celery_app = Celery(
    "app", backend=CELERY_BACKEND_URL, broker=CELERY_BROKER_URL, include=["app.tasks"],
)
celery_app.conf.task_routes = {"app.tasks.run_synspec": "synspec-queue"}
