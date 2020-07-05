import os
from celery import Celery
from celery.signals import after_task_publish

SYNSPEC_PATH = os.getenv("SYNSPEC_DIRPATH")

celery_app = Celery(
    "app",
    backend=os.getenv("CELERY_BACKEND_URL"),
    broker=os.getenv("CELERY_BROKER_URL"),
)
celery_app.conf.task_routes = {"app.tasks.run_synspec": "synspec-queue"}


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery_app.tasks.get(sender)
    backend = task.backend if task else celery_app.backend

    if backend.get_state(headers["id"]) == "PENDING":  # Task does not exists in backend
        backend.store_result(headers["id"], None, "SENT")
